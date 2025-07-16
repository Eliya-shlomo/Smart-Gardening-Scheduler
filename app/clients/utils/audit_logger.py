import requests

AUDIT_URL = "http://localhost:8003/audit_log/"

def send_log(
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int = None,
    details: str = None
):
    payload = {
        "user_id": user_id,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "details": details
    }
    try:
        response = requests.post(AUDIT_URL, json=payload, timeout=3)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send log to audit service: {e}")
