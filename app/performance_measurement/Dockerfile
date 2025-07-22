FROM python:3.11-slim

WORKDIR /app

COPY locust_users.py /app/

RUN pip install --no-cache-dir locust

CMD ["locust", "-f", "locust_users.py", "--host", "dummy"]
