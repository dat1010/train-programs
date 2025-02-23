import websocket
import json
import time

try:
    # Establish WebSocket connection
    ws = websocket.create_connection("ws://localhost:12080/json/")
    print("Connected via WebSocket")
    
    # Capture the initial "hello" message sent by the server
    hello_message = ws.recv()
    print("Hello message received:", hello_message)
    
    # Query the current power state by sending a power query command.
    power_query = {"type": "power"}
    ws.send(json.dumps(power_query))
    print("Sent power query command")
    
    # Receive the power state response
    power_response = ws.recv()
    print("Power response:", power_response)
   
    # Parse the power response
    power_data = json.loads(power_response)
    
    # Check if LocoNet is on (state == 2 indicates it's on)
    if "data" in power_data and power_data["data"].get("state") == 2:
        print("LocoNet is already ON.")
    else:
        print("LocoNet is OFF. Sending command to turn it ON.")
        power_on_command = {
            "type": "power",
            "data": {
                "name": "LocoNet",
                "state": 2   # 2 turns LocoNet ON
            }
        }
        ws.send(json.dumps(power_on_command))
        power_on_response = ws.recv()
        print("Power ON response:", power_on_response)
    
    # Now that LocoNet is on, send a throttle command (throttle 0.3 equals 30% throttle)
    throttle_command = {
        "type": "throttle",
        "data": {
            "address": "3",
            "speed": 0.15,
            "name": "3",       # Train identifier (adjust if needed)
            "throttle": "3"    # Throttle identifier (adjust if needed)
        }
    }
    ws.send(json.dumps(throttle_command))
    throttle_response = ws.recv()
    print("Throttle response:", throttle_response)
    
    # Wait 10 seconds before sending the next throttle command
    print("Waiting 10 seconds before setting throttle to -1...")
    time.sleep(10)
    
    # Send throttle command to set throttle to -1 (e.g., to stop or reverse)
    throttle_command_stop = {
        "type": "throttle",
        "data": {
            "address": "3",
            "speed": -1,
            "name": "3",
            "throttle": "3"
        }
    }
    ws.send(json.dumps(throttle_command_stop))
    throttle_stop_response = ws.recv()
    print("Throttle stop response:", throttle_stop_response)
    
    ws.close()
except Exception as e:
    print("Error:", e)
