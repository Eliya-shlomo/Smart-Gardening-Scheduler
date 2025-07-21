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
    options = ["נועה", "David", "רות", "Tom", "יוסי", "Sara"]
    return random.choice(options) + str(random.randint(100, 999))

def random_address():
    options = ["Herzl 12", "אלנבי 10", "Rothschild 22", "דיזנגוף 5", "King George 15"]
    return random.choice(options)

def random_phone():
    return ''.join(random.choices(string.digits, k=random.choice([9,10])))

def random_treatment():
    return random.choice(["טיפול פנים", "Facial", "שיקום עור", "Laser", "פילינג"])

def random_time():
    hour = random.randint(8, 18)
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02}:{minute:02}"

def random_notes():
    return random.choice(["הערה בעברית", "Some note", "שום דבר מיוחד", "ללא הערות", "בדיקה"])

def future_datetime(days=1):
    now = datetime.now()
    return (now + timedelta(days=random.randint(1, days+3))).strftime("%Y-%m-%dT%H:%M:%S")

class AppointmentsApiUser(HttpUser):
    host = "http://localhost:8006" 
    wait_time = between(1, 2)

    def on_start(self):
        self.email = random_email()
        self.password = random_password()
        self.name = random_name()
        self.phone = random_phone()
        self.token = None
        self.client_id = None
        self.appointments = []

        users_host = "http://localhost:8001"
        print("Registering user:", self.email)
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
        print("REGISTER USER status:", r.status_code, r.text)

        r = self.client.post(
            f"{users_host}/users/login",
            json={"email": self.email, "password": self.password},
            timeout=10
        )
        print("LOGIN USER status:", r.status_code, r.text)
        if r.status_code == 200:
            self.token = r.json().get("access_token")
        print("TOKEN:", self.token)

        clients_host = "http://localhost:8002"
        r = self.client.post(
            f"{clients_host}/clients/",
            json={
                "name": self.name,
                "email": self.email,
                "address": random_address(),
                "phone": random_phone(),
            },
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10
        )
        print("CREATE CLIENT status:", r.status_code, r.text)
        if r.status_code == 200:
            self.client_id = r.json()["id"]
        print("CLIENT_ID:", self.client_id)

    def _headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    @task
    def create_appointment(self):
        if not self.token or not self.client_id:
            print("Missing token or client_id in create_appointment")
            return
        with self.client.post(
            "/appointments",
            json={
                "client_id": self.client_id,
                "date": future_datetime(5),
                "time": random_time(),
                "treatment_type": random_treatment(),
                "notes": random_notes(),
                "status": "pending"
            },
            headers=self._headers(),
            catch_response=True
        ) as response:
            print("CREATE APPOINTMENT status:", response.status_code, response.text)
            if response.status_code == 200:
                app = response.json()
                self.appointments.append(app["id"])
                print("Created appointment:", app["id"])
            else:
                response.failure("Failed to create appointment")

    @task
    def get_client_appointments(self):
        if not self.token or not self.client_id:
            print("Missing token or client_id in get_client_appointments")
            return
        with self.client.get(
            f"/appointments/client/{self.client_id}",
            headers=self._headers(),
            catch_response=True
        ) as response:
            print("GET APPOINTMENTS status:", response.status_code, response.text)
            if response.status_code != 200:
                response.failure("Failed to get client appointments")

    @task
    def update_appointment(self):
        if not self.token or not self.client_id or not self.appointments:
            print("Cannot update appointment: missing token/client_id/appointments")
            return
        app_id = random.choice(self.appointments)
        with self.client.put(
            f"/appointments/{app_id}",
            json={
                "client_id": self.client_id,
                "date": future_datetime(5),
                "time": random_time(),
                "treatment_type": random_treatment(),
                "notes": random_notes(),
                "status": "pending"
            },
            headers=self._headers(),
            catch_response=True
        ) as response:
            print("UPDATE APPOINTMENT status:", response.status_code, response.text)
            if response.status_code != 200:
                response.failure("Failed to update appointment")

    @task
    def mark_appointment_done(self):
        if not self.token or not self.client_id or not self.appointments:
            print("Cannot mark appointment done: missing token/client_id/appointments")
            return
        app_id = random.choice(self.appointments)
        with self.client.patch(
            f"/appointments/{app_id}",
            json={
                "status": "done",
                "notes": random_notes()
            },
            headers=self._headers(),
            catch_response=True
        ) as response:
            print("MARK APPOINTMENT DONE status:", response.status_code, response.text)
            if response.status_code != 200:
                response.failure("Failed to mark appointment as done")

    @task
    def delete_appointment(self):
        if not self.token or not self.client_id or not self.appointments:
            print("Cannot delete appointment: missing token/client_id/appointments")
            return
        app_id = self.appointments.pop()
        with self.client.delete(
            f"/appointments/{app_id}",
            headers=self._headers(),
            catch_response=True
        ) as response:
            print("DELETE APPOINTMENT status:", response.status_code, response.text)
            if response.status_code != 200:
                response.failure("Failed to delete appointment")
