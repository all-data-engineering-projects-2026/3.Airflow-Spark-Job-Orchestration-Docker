FROM apache/airflow:2.10.3-python3.12

USER root

# Install system dependencies + Java 17 (for Apple Silicon / arm64)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc python3-dev \
    openjdk-17-jdk \
    procps \
    curl \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for Mac M5 Pro (arm64)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

# Create symlink for compatibility
RUN ln -s ${JAVA_HOME} /usr/lib/jvm/java-17-openjdk

USER airflow

# Upgrade pip and install Airflow + Spark provider + PySpark 4.0
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "apache-airflow==2.10.3" \
    apache-airflow-providers-apache-spark \
    "pyspark==4.0.0"

# Environment variables for PySpark consistency
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.7-src.zip:/opt/spark/python/lib/py4j-0.10.9.7-src.zip
