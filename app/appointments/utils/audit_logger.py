import requests

AUDIT_URL = "http://localhost:8003/audit_log/"

def send_log(user_id: int, action: str, entity_type: str, details: str, entity_id: int = None):
    payload = {
        "user_id": user_id,
        "action": action,
        "entity_type": entity_type,
        "details": details
    }
    if entity_id is not None:
        payload["entity_id"] = entity_id
    try:
        requests.post(AUDIT_URL, json=payload, timeout=2)
    except Exception as e:
        print("Could not send audit log:", e)

