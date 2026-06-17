from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    "owner": "himanshu",
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="sparking_flow",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["spark", "pyspark"],
) as dag:

    start = PythonOperator(
        task_id="start",
        python_callable=lambda: print("Spark Jobs Started"),
    )

    python_job = SparkSubmitOperator(
        task_id="python_job",
        conn_id="spark-conn",
        application="/opt/airflow/jobs/python/wordcount.py",
        name="wordcount-job",
        deploy_mode="client",
        verbose=True,
        conf={
            "spark.driver.memory": "1g",
            "spark.executor.memory": "1g",
            "spark.executor.cores": "1",
            "spark.driver.cores": "1",
            "spark.sql.adaptive.enabled": "true",
        },
    )

    end = PythonOperator(
        task_id="end",
        python_callable=lambda: print("Spark Jobs Completed Successfully"),
    )

    start >> python_job >> end