FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

WORKDIR /app
COPY notification/requirements.txt ./requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

COPY notification /app/notification

FROM python:3.11-slim AS final

WORKDIR /app
COPY --from=build /root/.local /root/.local
COPY --from=build /app /app

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "notification.main:app", "--host", "0.0.0.0", "--port", "8000"]
