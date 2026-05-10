import json
import websocket

GATEWAY_URL = "ws://127.0.0.1:18789"

def send_to_openclaw(intent_dict):
    try:
        ws = websocket.create_connection(GATEWAY_URL)

        message = {
            "type": "intent_check",
            "payload": intent_dict
        }

        ws.send(json.dumps(message))
        response = ws.recv()
        ws.close()

        return json.loads(response)

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    