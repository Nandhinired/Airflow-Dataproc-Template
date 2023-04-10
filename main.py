import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import DataprocInstantiateInlineWorkflowTemplateOperator



ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID","prod")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "project-gcp-378315")
REGION = os.environ.get("region", "europe-central2")

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

WORKFLOW_NAME = "airflow-dataproc-prod"
CLUSTER_NAME = f"cluster-dataproc-workflow-{ENV_ID}"

CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-4",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-4",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},

    },
}

WORKFLOW_TEMPLATE = {
    "id": WORKFLOW_NAME,
    "jobs": [
        {
            "spark_job": {
                "jar_file_uris": [
                    "gs://ingestionscalajar/Ingestdata-1.0-SNAPSHOT.jar"
                ],
                "properties": {
                    "spark.submit.deployMode": "client"
                },
                "args": [],
                "main_class": "Ingestdata.Ingestdata"
            },
            "step_id": "scala-spark-job",
        }
    ],
    "placement": {
        "managed_cluster": {
            "cluster_name": CLUSTER_NAME,
            "config": CLUSTER_CONFIG,
        }
    },

}

dag = DAG(
    'execute_scala_job_and_delete_cluster',
    default_args=default_args,
    description='Execute a Scala job in Dataproc and delete the cluster',
    schedule=None,
)


instantiate_template = DataprocInstantiateInlineWorkflowTemplateOperator(
    task_id='instantiate_template',
    template=WORKFLOW_TEMPLATE,
    project_id=PROJECT_ID,
    region=REGION,
    gcp_conn_id='google_cloud_default',
    dag=dag)

