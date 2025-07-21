
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
    options = ["עץ זית", "עץ רימון", "Olive", "Apple", "Orange"]
    return random.choice(options) + str(random.randint(100, 999))

def random_address():
    options = ["Herzl 12", "אלנבי 10", "Rothschild 22", "King George 15"]
    return random.choice(options)

def random_phone():
    return ''.join(random.choices(string.digits, k=random.choice([9,10])))

def random_recommendation_type():
    return random.choice(["השקיה", "דישון", "גיזום", "Watering", "Pruning", "Fertilizing"])

def random_notes():
    return random.choice(["להשקות", "דשן חצי כמות", "לא לגזום החודש", ""])

class RecommendationApiUser(HttpUser):
    host = "http://localhost:8006"  
    wait_time = between(1, 2)

    def on_start(self):
        self.email = random_email()
        self.password = random_password()
        self.name = random_name()
        self.phone = random_phone()
        self.token = None
        self.client_id = None
        self.tree_id = None
        self.recommendations = []

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
        # login
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

        trees_host = "http://localhost:8005/inventory"
        r = self.client.post(
            f"{trees_host}/trees/",
            json={
                "client_id": self.client_id,
                "type": random_name(),
                "planting_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "notes": random_notes(),
            },
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10
        )
        if r.status_code == 200:
            self.tree_id = r.json()["id"]

    def _headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    @task
    def create_recommendation(self):
        if not self.token or not self.tree_id:
            return
        with self.client.post(
            "/notification/recommendation/",
            json={
                "tree_id": self.tree_id,
                "type": random_recommendation_type(),
                "notes": random_notes(),
            },
            headers=self._headers(),
            catch_response=True
        ) as response:
            if response.status_code == 200:
                rec = response.json()
                self.recommendations.append(rec["id"])
            elif response.status_code == 400:
                response.success()
            else:
                response.failure("Failed to create recommendation")

    @task
    def get_all_recommendations(self):
        self.client.get(
            "/notification/recommendation/",
            headers=self._headers()
        )

    @task
    def get_recommendation_by_id(self):
        if not self.recommendations:
            return
        rec_id = random.choice(self.recommendations)
        self.client.get(
            f"/notification/recommendation/{rec_id}",
            headers=self._headers()
        )

    @task
    def delete_recommendation(self):
        if not self.recommendations:
            return
        rec_id = self.recommendations.pop()
        self.client.delete(
            f"/notification/recommendation/{rec_id}",
            headers=self._headers()
        )
