from locust import HttpUser, task, between
import random
import string

def random_action():
    return random.choice(["login", "logout", "register", "create", "update", "delete"])

def random_entity_type():
    return random.choice(["User", "Client", "Invoice", "Audit"])

def random_details():
    return random.choice([
        "User logged in",
        "Client created successfully",
        "Invoice approved",
        "Audit log written",
        "Some random event"
    ])

class AuditApiUser(HttpUser):
    host = "http://localhost:8003"  
    wait_time = between(1, 2)

    def on_start(self):

        self.user_id = random.randint(1, 1000)
        self.logs_created = []

    @task
    def create_log(self):
        action = random_action()
        entity_type = random_entity_type()
        entity_id = random.randint(1, 200)
        details = random_details()

        with self.client.post(
            "/audit_log/",
            json={
                "user_id": self.user_id,
                "action": action,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "details": details,
            },
            catch_response=True
        ) as response:
            if response.status_code == 201:
                log = response.json()
                self.logs_created.append(log["id"])
            else:
                response.failure("Failed to create log")

    @task
    def get_my_logs(self):
        params = {"user_id": self.user_id}
        self.client.get("/audit_log/", params=params)
