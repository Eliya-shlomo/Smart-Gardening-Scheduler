from locust import HttpUser, task, between
import random
import string

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"

def random_password():
    letters = string.ascii_letters + string.digits + " _-!@#$%^&*()+=."
    return ''.join(random.choices(letters, k=10))

def random_name():
    options = ["דנה", "Noam", "משה", "Sara", "יוסי", "Tom", "רותם", "Lior"]
    return random.choice(options) + str(random.randint(10, 99))

def random_phone():
    length = random.choice([9, 10])
    return ''.join(random.choices(string.digits, k=length))

class UserApiUser(HttpUser):
    host = "http://localhost:8001"  
    wait_time = between(1, 2)

    def on_start(self):
        self.email = random_email()
        self.password = random_password()
        self.name = random_name()
        self.phone = random_phone()
        self.token = None
        self.refresh_token = None

        with self.client.post("/users/register", json={
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
            "password": self.password,
        }, catch_response=True) as response:
            if response.status_code == 200:
                pass  
            elif response.status_code == 400:
                response.success()
            else:
                response.failure("Registration failed: " + str(response.text))

        with self.client.post("/users/login", json={
            "email": self.email,
            "password": self.password,
        }, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.refresh_token = data.get("refresh_token")
            else:
                response.failure("Login failed: " + str(response.text))

    @task
    def get_me(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/users/me", headers=headers)

    @task
    def refresh_access_token(self):
        if self.refresh_token:
            with self.client.post(
                "/users/refresh-token",
                data=f'"{self.refresh_token}"',
                headers={"Content-Type": "application/json"},
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    data = response.json()
                    self.token = data["access_token"]
                else:
                    self.refresh_token = None
                    response.failure("Refresh token failed: " + str(response.text))

    @task
    def logout(self):
        if self.refresh_token:
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            with self.client.post(
                "/users/logout",
                data=f'"{self.refresh_token}"',
                headers=headers,
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    self.token = None
                    self.refresh_token = None
                else:
                    self.refresh_token = None
                    response.failure("Logout failed: " + str(response.text))
