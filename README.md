# Using DataprocInstantiateTemplateOperator in Composer (Airflow) for Dataproc Cluster Automation

![image](https://github.com/Nandhinired/Airflow-Dataproc-Template/assets/69593809/637a83c2-1f4f-4c62-88d2-62b2cb75e16d)
This README provides instructions for using the DataprocInstantiateTemplateOperator in Google Composer / Apache Airflow to automate cluster provisioning and management using Google Cloud Dataproc.

## Configuration
Configure the required parameters in your DAG file:
   * project_id: Google Cloud project ID.
   * region: Google Cloud region where the Dataproc cluster will be created.
   * template_id: ID of the Dataproc cluster template to use.
   * cluster_name: Name of the cluster to be created.
   * job_name: Unique name for the Airflow task.
   * wait_interval: Interval in seconds to check the cluster operation status.

## Additional Notes
* Ensure that the necessary IAM permissions are granted to the service account used for authentication.
* You can customize the DAG and add additional tasks to perform specific operations on the Dataproc cluster.
* Consult the Airflow documentation for more details on DAG configuration and scheduling.
