using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class CPHInline
{
    public bool Execute()
    {
        // Run the asynchronous JMRI command synchronously.
        RunJmriCommandAsync().GetAwaiter().GetResult();
        return true;
    }
    
    private async Task RunJmriCommandAsync()
    {
        using (ClientWebSocket ws = new ClientWebSocket())
        {
            var uri = new Uri("ws://rpi-jmri.local:12080/json/");
            await ws.ConnectAsync(uri, CancellationToken.None);
            Console.WriteLine("Connected via WebSocket");

            // Capture the initial "hello" message sent by the server.
            string helloMessage = await ReceiveString(ws);
            Console.WriteLine("Hello message received: " + helloMessage);

            // Query the current power state.
            var powerQuery = new { type = "power" };
            await SendString(ws, JsonConvert.SerializeObject(powerQuery));
            Console.WriteLine("Sent power query command");

            string powerResponse = await ReceiveString(ws);
            Console.WriteLine("Power response: " + powerResponse);

            // Parse the power response using JObject.
            var powerData = JObject.Parse(powerResponse);
            bool locoOn = false;
            if (powerData["data"] != null && powerData["data"]["state"] != null)
            {
                if ((int)powerData["data"]["state"] == 2)
                {
                    locoOn = true;
                    Console.WriteLine("LocoNet is already ON.");
                }
            }
            if (!locoOn)
            {
                Console.WriteLine("LocoNet is OFF. Sending command to turn it ON.");
                var powerOnCommand = new
                {
                    type = "power",
                    data = new
                    {
                        name = "LocoNet",
                        state = 2   // 2 turns LocoNet ON
                    }
                };
                await SendString(ws, JsonConvert.SerializeObject(powerOnCommand));
                string powerOnResponse = await ReceiveString(ws);
                Console.WriteLine("Power ON response: " + powerOnResponse);
            }

            // Send throttle command to set throttle to 0.15 (15% throttle).
            var throttleCommand = new
            {
                type = "throttle",
                data = new
                {
                    address = "3",
                    speed = 0.15,
                    name = "3",       // Train identifier (adjust if needed)
                    throttle = "3"    // Throttle identifier (adjust if needed)
                }
            };
            await SendString(ws, JsonConvert.SerializeObject(throttleCommand));
            string throttleResponse = await ReceiveString(ws);
            Console.WriteLine("Throttle response: " + throttleResponse);

            // Wait 10 seconds before sending the next throttle command.
            Console.WriteLine("Waiting 10 seconds before setting throttle to -1...");
            await Task.Delay(10000);

            // Send throttle command to set throttle to -1 (e.g., to stop or reverse).
            var throttleCommandStop = new
            {
                type = "throttle",
                data = new
                {
                    address = "3",
                    speed = -1,
                    name = "3",
                    throttle = "3"
                }
            };
            await SendString(ws, JsonConvert.SerializeObject(throttleCommandStop));
            string throttleStopResponse = await ReceiveString(ws);
            Console.WriteLine("Throttle stop response: " + throttleStopResponse);

            // Finally, send a command to turn LocoNet OFF (state 4).
            var powerOffCommand = new
            {
                type = "power",
                data = new
                {
                    name = "LocoNet",
                    state = 4   // 4 turns LocoNet OFF
                }
            };
            await SendString(ws, JsonConvert.SerializeObject(powerOffCommand));
            string powerOffResponse = await ReceiveString(ws);
            Console.WriteLine("Power OFF response: " + powerOffResponse);

            await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", CancellationToken.None);
        }
    }

    private async Task SendString(ClientWebSocket ws, string message)
    {
        byte[] bytes = Encoding.UTF8.GetBytes(message);
        await ws.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, CancellationToken.None);
    }

    private async Task<string> ReceiveString(ClientWebSocket ws)
    {
        var buffer = new ArraySegment<byte>(new byte[1024]);
        using (var ms = new MemoryStream())
        {
            WebSocketReceiveResult result;
            do
            {
                result = await ws.ReceiveAsync(buffer, CancellationToken.None);
                ms.Write(buffer.Array, buffer.Offset, result.Count);
            }
            while (!result.EndOfMessage);

            ms.Seek(0, SeekOrigin.Begin);
            using (var reader = new StreamReader(ms, Encoding.UTF8))
            {
                return await reader.ReadToEndAsync();
            }
        }
    }
}
