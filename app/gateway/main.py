from fastapi import FastAPI, Request, Depends, HTTPException
from gateway.proxy import proxy_request
from gateway.auth import verify_jwt_token

app = FastAPI()

# ---------------------------------------
# AUTH ROUTES (proxy to users service)
# ---------------------------------------

# Login endpoint: proxies to users service
@app.post("/auth/login")
async def login(request: Request):
    return await proxy_request(request, service_name="users", path="/login")

# Register endpoint: proxies to users service
@app.post("/auth/register")
async def register(request: Request):
    return await proxy_request(request, service_name="users", path="/register")

# ---------------------------------------
# USERS ROUTES (proxy to users service)
# ---------------------------------------

# Get current user info (requires JWT token)
@app.get("/users/me")
async def get_me(token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="users", path="/me")

# Update current user info (requires JWT token)
@app.put("/users/me")
async def update_me(request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="users", path="/me")

# ---------------------------------------
# CLIENTS ROUTES (proxy to clients service)
# ---------------------------------------

# Get all clients (requires JWT token)
@app.get("/clients/")
async def get_clients(token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="clients", path="/clients")

# Create a new client (requires JWT token)
@app.post("/clients/")
async def create_client(request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="clients", path="/clients")

# Get a specific client by ID (requires JWT token)
@app.get("/clients/{client_id}")
async def get_client(client_id: int, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="clients", path=f"/clients/{client_id}")

# ---------------------------------------
# SCHEDULER ROUTES (proxy to scheduler service)
# ---------------------------------------

# Get all appointments (requires JWT token)
@app.get("/scheduler/appointments")
async def get_appointments(token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="scheduler", path="/appointments")

# Create a new appointment (requires JWT token)
@app.post("/scheduler/appointments")
async def create_appointment(request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="scheduler", path="/appointments")

# Update an appointment (requires JWT token)
@app.put("/scheduler/appointments/{appointment_id}")
async def update_appointment(appointment_id: int, request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="scheduler", path=f"/appointments/{appointment_id}")

# Delete an appointment (requires JWT token)
@app.delete("/scheduler/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="scheduler", path=f"/appointments/{appointment_id}")

# ---------------------------------------
# INVENTORY ROUTES (proxy to inventory service)
# ---------------------------------------

# Get inventory items (requires JWT token)
@app.get("/inventory/items")
async def get_inventory(token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="inventory", path="/items")

# Add a new inventory item (requires JWT token)
@app.post("/inventory/items")
async def add_item(request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="inventory", path="/items")

# Update an inventory item (requires JWT token)
@app.put("/inventory/items/{item_id}")
async def update_item(item_id: int, request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="inventory", path=f"/items/{item_id}")

# Delete an inventory item (requires JWT token)
@app.delete("/inventory/items/{item_id}")
async def delete_item(item_id: int, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="inventory", path=f"/items/{item_id}")

# ---------------------------------------
# NOTIFICATION ROUTES (proxy to notification service)
# ---------------------------------------

# Send a notification (optional, requires JWT token)
@app.post("/notification/send")
async def send_notification(request: Request, token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="notification", path="/send")

# ---------------------------------------
# AUDIT ROUTES (proxy to audit service)
# ---------------------------------------

# Get audit logs/history (requires JWT token)
@app.get("/audit/logs")
async def get_audit_logs(token_data=Depends(verify_jwt_token)):
    return await proxy_request(request, service_name="audit", path="/logs")
