FROM python:3.11-slim AS build

WORKDIR /app

COPY users/requirements.txt ./users/requirements.txt
RUN pip install --user --no-cache-dir -r users/requirements.txt

COPY users ./users

FROM python:3.11-slim AS final

WORKDIR /app

COPY --from=build /root/.local /root/.local
COPY --from=build /app /app

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "users.main:app", "--host", "0.0.0.0", "--port", "8000"]
