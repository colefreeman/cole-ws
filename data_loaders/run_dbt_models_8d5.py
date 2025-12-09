import subprocess
import os


@data_loader
def run_dbt_models(project_dir: str, *args, **kwargs):
    """
    Executes dbt commands within Mage, leveraging source references for lineage tracking.

    Args:
        project_dir (str): Path to the local dbt project directory.
        command (str): The dbt CLI command to execute, default is 'dbt run'.
        **kwargs: Additional keyword arguments for flexibility.

    Returns:
        None
    """

    command: str = "dbt run"

    # Change working directory to the dbt project directory
    os.chdir(project_dir)

    # Construct the dbt command
    dbt_command = command

    # Execute the dbt command
    process = subprocess.Popen(
        dbt_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Capture output and errors
    stdout, stderr = process.communicate()

    # Decode and print output for logging purposes
    print(stdout.decode("utf-8"))
    if stderr:
        print(stderr.decode("utf-8"))

    # Check for successful execution
    if process.returncode != 0:
        raise RuntimeError(f"dbt command failed with exit code {process.returncode}")
