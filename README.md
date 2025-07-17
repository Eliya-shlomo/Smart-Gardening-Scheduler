# Smart Gardening Scheduler 🌱

**Smart Gardening Scheduler** is a full-stack, cloud-ready solution for professional gardeners and gardening businesses, providing client management, scheduling, automation, recommendations, and a smooth experience for both gardener and client.

---

## 🚀 Main Goals

- Enable easy and secure management of clients, appointments, trees, and equipment
- Improve the client’s experience with automation (recommendations, reminders, reports)
- Deliver a modern, scalable, microservice-ready platform (Monorepo)

---

## 🏗️ Architecture & Technologies

- **Monorepo:** Microservice-ready codebase, each service in a separate folder (`users`, `clients`, `scheduler`, etc.)
- **Services:** Each domain (Users, Clients, Scheduler, Audit) is logically separated and will be deployed independently in the future
- **API Gateway:** Nginx reverse proxy manages all traffic and routes to services (current/future)
- **Database:** PostgreSQL with Alembic for schema migrations
- **DevOps:** Jenkins + Docker + Kubernetes + AWS ECR for CI/CD and deployment

---

## 🛠️ Tech Stack

| Technology      | Main Use                        |
|-----------------|---------------------------------|
| **FastAPI**     | Modern backend API              |
| **PostgreSQL**  | Main relational database        |
| **Alembic**     | Database migrations             |
| **Docker**      | Containerization                |
| **Kubernetes**  | Deployment & scaling            |
| **AWS ECR**     | Docker image storage            |
| **Jenkins**     | CI/CD automation                |
| **Nginx**       | API Gateway & proxy             |
| **dotenv**      | Environment & secrets management|

---

## 🗂️ Repository Structure
```bash

Smart-Gardening-Scheduler/
│
├── app/ # API code (services in subfolders)
│ ├── clients/
│ ├── users/
│ ├── scheduler/
│ └── ...
│
├── frontend/ # (WIP) React Native (Expo) mobile app
│
├── alembic/ # Alembic migrations
│
├── k8s/ # Kubernetes YAML manifests
│
├── nginx/ # Nginx proxy config
│
├── scripts/ # CI/CD scripts and utilities
│
├── tests/ # Automated & integration tests
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md

markdown
Copy
Edit
```
---

## ✨ Features

- **User Authentication:** Secure registration & login with JWT tokens and Bcrypt password hashing
- **Client & Garden Management:** Track clients, addresses, trees/plants, equipment, and more
- **Appointments:** Schedule, update, and manage gardening jobs & appointments
- **Automated Recommendations:** Personalized care tips and seasonal reminders for gardeners & clients
- **Audit Logging:** All important actions are logged for transparency and traceability
- **Notifications:** Ready for real-time email notifications (SMTP configurable)
- **Modern Mobile App:** (WIP) Cross-platform frontend using React Native (Expo)
- **DevOps Excellence:** Full CI/CD pipeline with Jenkins, Docker, ECR, and Kubernetes
- **Scalable Microservices:** Designed to evolve from monolith to microservices easily

---

## ⚡️ Quick Start

### 1. Prerequisites

- Python 3.10+
- Node.js (for Expo frontend)
- Docker
- PostgreSQL database (or run via Docker)

### 2. Database with Docker (Recommended)

```bash
docker run -d --name gardening-postgres -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=gardening_db \
  postgres:13
```


### Clone the Repository
```bash
git clone https://github.com/Eliya-shlomo/Smart-Gardening-Scheduler.git
cd Smart-Gardening-Scheduler
```

### Configure Environment Variables
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gardening_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=gardening_db
SMTP_SERVER=<your_smtp_server>      # e.g. smtp.gmail.com
SMTP_PORT=<your_smtp_port>          # e.g. 587
SMTP_USERNAME=<your_email_username>
SMTP_PASSWORD=<your_email_password>
MAIL_FROM=<sender_email_address>
JWT_SECRET=<your_super_secret>
```

### Install Backend Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Run each Microservice

```bash
uvicorn {microservice_name}.main:app --reload --port 8000
```

### Running end to end Tests

```bash
cd app/{microservice_name}
pytest
```

### Run the Frontend App

```bash
cd frontend
npm install
npx expo start
```

### Example API Usage
```bash
POST /users/register
{
  "name": "Alice Gardener",
  "email": "alice@example.com",
  "phone": "0521234567",
  "password": "SecurePass123"
}
Login:

json
Copy
Edit
POST /users/login
{
  "email": "alice@example.com",
  "password": "SecurePass123"
}
Create Client:

json
Copy
Edit
POST /clients/
{
  "name": "Green Villa",
  "email": "owner@greenvilla.com",
  "address": "123 Garden Lane",
  "phone": "0511111111"
}
Add Tree:

json
Copy
Edit
POST /trees/
{
  "type": "Mango",
  "planting_date": "2025-07-17T21:00:00Z",
  "notes": "Near fence.",
  "client_id": 7
}
```
---
### Security

* All sensitive data and credentials are managed via environment variables or Kubernetes secrets.

* Passwords are stored using Bcrypt hashing.

* JWT tokens are required for protected endpoints.

---
### DevOps & CI/CD

* Jenkins automates build, test, and deployment pipelines.

* Docker builds and runs all services as containers.

* AWS ECR is used for image storage.

* Kubernetes orchestrates deployment, scaling, and secrets management.

* Nginx routes all API and static traffic.

---

### Extending the Project

* Add more microservices (e.g., Payments, Reports, IoT Sensors)

* Improve recommendation engine (AI/ML)

* Enhance frontend with advanced UI/UX

* Add calendar and notification integrations