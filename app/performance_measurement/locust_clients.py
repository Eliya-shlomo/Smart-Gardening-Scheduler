from locust import HttpUser, task, between
import random
import string

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"

def random_name():
    options = ["חנה", "David", "רות", "Tom", "יוסי", "Sara"]
    return random.choice(options) + str(random.randint(100, 999))

def random_address():
    options = ["Herzl 12", "אלנבי 10", "Rothschild 22", "דיזנגוף 5", "King George 15"]
    return random.choice(options)

def random_phone():
    return ''.join(random.choices(string.digits, k=random.choice([9,10])))

def random_password():
    letters = string.ascii_letters + string.digits + " _-!@#$%^&*()+=."
    return ''.join(random.choices(letters, k=10))

class ClientApiUser(HttpUser):
    host = "http://localhost:8002"  
    wait_time = between(1, 2)

    def on_start(self):

        self.email = random_email()
        self.password = random_password()
        self.name = random_name()
        self.phone = random_phone()

        users_host = "http://localhost:8001"
        # register
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
        # login
        r = self.client.post(
            f"{users_host}/users/login",
            json={"email": self.email, "password": self.password},
            timeout=10
        )
        if r.status_code == 200:
            tokens = r.json()
            self.token = tokens.get("access_token")
        else:
            self.token = None

        self.clients_created = []  
    @task
    def create_client(self):
        if not self.token:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        name = random_name()
        email = random_email()
        address = random_address()
        phone = random_phone()

        with self.client.post(
            "/clients/",
            json={
                "name": name,
                "email": email,
                "address": address,
                "phone": phone,
            },
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                client = response.json()
                self.clients_created.append(client["id"])
            else:
                response.failure("Failed to create client")

    @task
    def get_clients(self):
        if not self.token:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/clients/", headers=headers)

    @task
    def update_client(self):
        if not self.token or not self.clients_created:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        client_id = random.choice(self.clients_created)
        new_name = random_name()
        new_email = random_email()
        new_address = random_address()
        new_phone = random_phone()
        self.client.put(
            f"/clients/{client_id}",
            json={
                "name": new_name,
                "email": new_email,
                "address": new_address,
                "phone": new_phone,
            },
            headers=headers
        )

    @task
    def delete_client(self):
        if not self.token or not self.clients_created:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        client_id = self.clients_created.pop()
        self.client.delete(f"/clients/{client_id}", headers=headers)

    @task
    def check_access(self):
        if not self.token or not self.clients_created:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        client_id = random.choice(self.clients_created)
        self.client.get(f"/clients/{client_id}/access", headers=headers)
