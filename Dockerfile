FROM python:3.10-slim AS builder

RUN apt-get update
WORKDIR /app

COPY . .

RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

EXPOSE 8000

ENV POSTGRE_USER hackaton
ENV POSTGRE_PASSWORD hackaton
ENV POSTGRE_PORT 5432
ENV POSTGRE_IP database-svc
ENV POSTGRE_DB hackaton

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
