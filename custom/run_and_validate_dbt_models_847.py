import subprocess
import sys


@custom
def run_and_validate_dbt_models(data: None, *args, **kwargs):
    """
    Executes dbt models to validate source references and ensure models are up-to-date.
    """

    # Run dbt models using subprocess to invoke 'dbt run'
    try:
        result = subprocess.run(
            ["dbt", "run"],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except subprocess.CalledProcessError as e:
        # Log error if dbt run fails
        print(f"Error running dbt models: {e}")
        raise

    # Optionally, parse output or logs here for further validation
    print(
        "dbt models executed successfully. Please review logs for any source-related errors."
    )
