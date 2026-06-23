# Apache Airflow + Spark Standalone Cluster

**Production-Ready Docker Setup for Orchestrating PySpark Jobs with Apache Airflow**

---

## 📌 Project Overview

This project provides a **complete, containerized environment** for running **Apache Airflow** and **Apache Spark** together. It demonstrates how to orchestrate PySpark jobs using Airflow's `SparkSubmitOperator` in a local development setup.

**Goal:** Submit and run PySpark applications (e.g., WordCount) from Airflow DAGs to a Spark cluster, all running inside Docker.

---

## 🏗️ Architecture

```
┌──────────────────────────────┐
│     Apache Airflow           │
│  (Webserver + Scheduler)     │
│  - DAG: sparking_flow        │
│  - SparkSubmitOperator       │
└──────────────┬───────────────┘
               │ spark-submit
               ▼
┌──────────────────────────────┐
│     Apache Spark Cluster     │
│  - Spark Master (port 7077)  │
│  - Spark Workers (x2)        │
│  - PySpark 4.0               │
└──────────────────────────────┘
               │
               ▼
         Shared Volume
         (jobs/ + dags/)
```

**Key Components:**
- **Docker Compose** orchestration
- **Shared volumes** between Airflow and Spark containers
- **Custom Docker images** with Java 17 (arm64 compatible)
- **PostgreSQL** as Airflow metadata database

---

## 🛠️ Technology Stack

| Component              | Technology                     | Version     | Role |
|------------------------|--------------------------------|-------------|------|
| **Orchestration**      | Apache Airflow                 | 2.10.3      | DAG scheduling & Spark job submission |
| **Compute Engine**     | Apache Spark (Standalone)      | 4.0.0       | PySpark job execution |
| **Language**           | Python + PySpark               | 3.12 / 4.0  | Job development |
| **Containerization**   | Docker + Docker Compose        | -           | Multi-service environment |
| **Database**           | PostgreSQL                     | 14          | Airflow metadata store |
| **Job Submission**     | SparkSubmitOperator            | -           | Airflow → Spark integration |

---

## ✨ Key Features

- **Full Spark + Airflow Integration** — Submit PySpark jobs directly from Airflow using `SparkSubmitOperator`
- **Compatible** — Custom Dockerfiles with Java 17
- **Modern Python Environment** — Python 3.12 + PySpark 4.0
- **Shared Volumes** — Easy access to job scripts from both Airflow and Spark
- **Production-Ready Docker Setup** — Clean separation of services
- **Example DAG** — Ready-to-use `sparking_flow` DAG with start → submit → end pattern
- **Detailed Documentation** — Includes troubleshooting and best practices

---

## 📁 Project Structure

```
Apache_Airflow_with_Spark/
├── docker-compose.yml              # Main orchestration file
├── Dockerfile                      # Airflow image (with Java 17)
├── Dockerfile.spark                # Spark image (Python 3.12 + PySpark 4.0)
├── airflow.env                     # Airflow configuration
├── airflow.env.example
│
├── dags/
│   └── spark_airflow.py            # Main DAG using SparkSubmitOperator
│
├── jobs/
│   └── python/
│       └── wordcount.py            # Example PySpark WordCount job
│
├── project_snapshots/              # Execution screenshots
├── Airflow_Pyspark_DE_project_details.pdf   # Detailed documentation
└── README.md
```

---

## 🔄 How It Works

1. **DAG Triggered** → `sparking_flow` DAG starts
2. **Start Task** → Simple PythonOperator prints start message
3. **Spark Job Submission** → `SparkSubmitOperator` submits `wordcount.py` to Spark Master
4. **Spark Execution** → Spark Master distributes the job to workers
5. **End Task** → PythonOperator confirms completion
6. **Monitoring** → View results in Airflow logs + Spark Master UI

---

## 🚀 Getting Started

### 1. Clone and Prepare Environment

```bash
git clone <your-repo-url>
cd Apache_Airflow_with_Spark

cp airflow.env.example airflow.env
# Edit airflow.env and set a strong SECRET_KEY
```

### 2. Build and Start Services

```bash
docker compose down -v --remove-orphans
docker compose build --no-cache
docker compose up -d
```

### 3. Access UIs

| Service          | URL                        | Credentials      |
|------------------|----------------------------|------------------|
| **Airflow UI**   | http://localhost:8080      | admin / admin    |
| **Spark Master** | http://localhost:9090      | -                |

### 4. Configure Spark Connection in Airflow

1. Go to **Admin → Connections**
2. Create new connection:
   - **Conn Id**: `spark-conn`
   - **Conn Type**: `Spark`
   - **Spark Binary**: `spark-submit`
   - **Master**: `spark://spark-master:7077`
   - **Deploy Mode**: `client`

### 5. Trigger the DAG

- Go to DAGs → `sparking_flow`
- Trigger manually
- Monitor execution in Airflow and Spark UI

---

## 🧠 Skills Demonstrated

- Building multi-container environments with Docker Compose
- Integrating **Apache Airflow** with **Apache Spark** using `SparkSubmitOperator`
- Writing and packaging PySpark applications
- Custom Docker image creation (Java + Python compatibility)
- Volume mounting strategies for code sharing
- Production-grade local development setup for data engineering

---

## ⚠️ Common Issues & Solutions

| Issue                        | Solution |
|-----------------------------|----------|
| `JAVA_HOME` not set         | Dockerfile installs OpenJDK 17 and sets `JAVA_HOME` |
| File not found              | Ensure `jobs/` volume is correctly mounted in both services |
| Connection refused          | Verify Spark Master is reachable at `spark://spark-master:7077` |
| Permission errors           | Check file permissions inside containers |
| `deploy_mode=cluster` fails | Use `client` mode for PySpark on standalone clusters (as done in DAG) |

---

## 📄 License

This project is created for **learning and portfolio demonstration** purposes.

---

**Author:** Himanshu  
**Focus:** Apache Airflow + Apache Spark Integration | Docker-based Data Engineering Environments

---

*Built with modern data engineering best practices using Docker, Airflow, and Spark.*