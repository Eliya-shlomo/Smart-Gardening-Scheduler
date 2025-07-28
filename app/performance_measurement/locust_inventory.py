from locust import HttpUser, task, between
import random
import string
from datetime import datetime, timedelta

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"

def random_password():
    letters = string.ascii_letters + string.digits + " _-!@#$%^&*()+=."
    return ''.join(random.choices(letters, k=10))

def random_name():
    options = ["עץ זית", "עץ תפוז", "עץ רימון", "עץ שקמה", "Olive", "Apple"]
    return random.choice(options) + str(random.randint(100, 999))

def random_address():
    options = ["Herzl 12", "אלנבי 10", "Rothschild 22", "דיזנגוף 5", "King George 15"]
    return random.choice(options)

def random_phone():
    return ''.join(random.choices(string.digits, k=random.choice([9, 10])))

def random_notes():
    return "pikabu"

def future_datetime(days=1):
    now = datetime.now()
    return (now + timedelta(days=random.randint(1, days+3))).strftime("%Y-%m-%dT%H:%M:%S")

class TreesApiUser(HttpUser):
    host = "http://localhost:8005"
    wait_time = between(1, 2)

    def on_start(self):
        self.email = random_email()
        self.password = random_password()
        self.name = random_name()
        self.phone = random_phone()
        self.token = None
        self.client_id = None
        self.trees = []

        users_host = "http://localhost:8001"
        r = self.client.post(
            f"{users_host}/users/register",
            json={
                "email": self.email,
                "name": self.name,
                "phone": self.phone,
                "password": self.password,
            },
            timeout=10
        )

        r = self.client.post(
            f"{users_host}/users/login",
            json={"email": self.email, "password": self.password},
            timeout=10
        )
        if r.status_code == 200:
            self.token = r.json().get("access_token")

        clients_host = "http://localhost:8002"
        r = self.client.post(
            f"{clients_host}/clients/",
            json={
                "name": random_name(),
                "email": random_email(),
                "address": random_address(),
                "phone": random_phone(),
            },
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10
        )
        if r.status_code == 200:
            self.client_id = r.json()["id"]

    def _headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    @task
    def create_tree(self):
        if not self.token or not self.client_id:
            return
        with self.client.post(
            "/inventory/trees/",
            json={
                "client_id": self.client_id,
                "type": random_name(),
                "planting_date": future_datetime(90),
                "notes": random_notes(),
            },
            headers=self._headers(),
            catch_response=True
        ) as response:
            if response.status_code == 200:
                tree = response.json()
                self.trees.append(tree["id"])
            else:
                response.failure("Failed to create tree")

    @task
    def get_trees_for_client(self):
        if not self.token or not self.client_id:
            print("Missing token or client_id")
            return
        with self.client.get(
            f"/inventory/trees/client/{self.client_id}",
            headers=self._headers(),
            catch_response=True
        ) as response:
            print("GET trees/client status:", response.status_code)
            if response.status_code != 200:
                print(response.text)
                response.failure("Failed to get trees for client")

    @task
    def update_tree(self):
        if not self.token or not self.client_id or not self.trees:
            return
        tree_id = random.choice(self.trees)
        with self.client.put(
            f"/inventory/trees/{tree_id}",
            json={
                "type": random_name(),
                "planting_date": future_datetime(100),
                "notes": random_notes(),
            },
            headers=self._headers(),
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("Failed to update tree")

    @task
    def get_tree_by_id(self):
        if not self.token or not self.client_id or not self.trees:
            return
        tree_id = random.choice(self.trees)
        self.client.get(
            f"/inventory/trees/{tree_id}",
            headers=self._headers()
        )

    @task
    def delete_tree(self):
        if not self.token or not self.client_id or not self.trees:
            return
        tree_id = self.trees.pop()
        self.client.delete(
            f"/inventory/trees/{tree_id}",
            headers=self._headers()
        )
