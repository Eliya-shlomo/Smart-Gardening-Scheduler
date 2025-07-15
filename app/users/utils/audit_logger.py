import requests

AUDIT_LOG_URL = "http://auditlog-service/audit-log/"  

def send_audit_log(user_id: int, action: str, entity_type: str, details: str):
    payload = {
        "user_id": user_id,
        "action": action,
        "entity_type": entity_type,
        "details": details
    }
    try:
        requests.post(AUDIT_LOG_URL, json=payload, timeout=2)
    except Exception as e:
        print("Could not send audit log:", e)
