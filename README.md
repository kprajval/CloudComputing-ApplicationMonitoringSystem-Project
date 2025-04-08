# CloudComputing-ApplicationMonitoringSystem-Project

This project is a basic **Application Monitoring System** built using **Apache Kafka**, **PostgreSQL**, **Docker**, and **Grafana**. It simulates logs from a running application, streams them via Kafka, stores them in PostgreSQL, and visualizes metrics in Grafana. This porject was built on Kali linux system.

---

## 📁 Project Structure

```
ApplicationMonitoringSystem/
├── app.py              # Sample app for generating logs
├── producer.py         # Kafka producer sending logs to topic
├── simulation.py       # Simulates user activity (requests)
├── consumer.py         # Kafka consumer storing logs into PostgreSQL
├── docker-compose.yml  # Optional (not used here but can be for orchestration)
└── README.md           # This file
```

---

## 🚀 Week 1: Setup & Log Generation

### ✅ Kafka Setup
- **Kafka topic** was created manually.
- Logs are published via `producer.py` using Kafka's Python client.
- Example log message format:
  ```json
  {
    "log": "2025-04-07 12:55:40,426 - GET /status"
  }
  ```

---

## 🏗️ Week 2: Log Processing and Storage

### ✅ PostgreSQL with Docker

Start PostgreSQL using Docker:
```bash
docker run --name my-postgres -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres
```

### ✅ Kafka Consumer

`consumer.py` reads from Kafka and inserts logs into the `logs` table in PostgreSQL.

#### PostgreSQL Table Schema

```sql
CREATE TABLE logs (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP,
  method VARCHAR(10),
  endpoint TEXT,
  status_code INT
);
```

Logs are parsed and inserted after extracting timestamp, method, endpoint, and status code.

---

## 📊 Week 3: Visualization in Grafana

### ✅ Grafana Docker Setup

```bash
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

### ✅ Docker Networking (Optional Step to connect containers)

```bash
docker network create monitoring-net
docker network connect monitoring-net my-postgres
docker network connect monitoring-net grafana
```

### ✅ Connect PostgreSQL to Grafana

1. Go to `http://localhost:3000`
2. Login: `admin / admin`
3. Add PostgreSQL as a new **data source** using:
   - Host: `my-postgres:5432`
   - User: `postgres`
   - Password: `admin`
   - Database: `postgres`

---

## 📈 Dashboards and Queries

### 🔸 1. All Logs

```sql
SELECT * FROM logs;
```

### 🔸 2. Count Total Logs

```sql
SELECT COUNT(*) FROM logs;
```

### 🔸 3. Bar Chart: Top Endpoints

```sql
SELECT endpoint, COUNT(*) AS hits
FROM logs
GROUP BY endpoint
ORDER BY hits DESC
LIMIT 5;
```

### 🔸 4. Pie Chart: Status Code Breakdown

```sql
SELECT status_code, COUNT(*) AS total
FROM logs
GROUP BY status_code
ORDER BY status_code;
```

### 🔸 5. Time Series: Requests Per Minute

```sql
SELECT
  date_trunc('minute', timestamp) AS time,
  COUNT(*) AS count
FROM logs
GROUP BY time
ORDER BY time;
```

---

## 🔍 Monitoring Features Implemented

- Real-time logging from a Python app
- Log ingestion through Kafka
- Log parsing and transformation
- PostgreSQL log storage
- Grafana dashboards with:
  - Bar chart (Top Endpoints)
  - Pie chart (Status Code Breakdown)
  - Time Series (Log Volume Over Time)

---

## 🚫 Known Issues / Future Improvements

- Add Docker Compose to manage multi-container setup.
- Add alerting and notifications in Grafana.
- Extend log schema with user agents, IPs, etc.
- Support for log severity (INFO, ERROR, etc.)

---

## 🧑‍💻 Author

This project is part of a weekly internship task focused on real-time monitoring and visualization of application logs.

---

