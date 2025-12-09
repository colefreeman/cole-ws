import os
import subprocess


@data_loader
def clone_your_dbt_repo(*args, **kwargs):
    """
    Clone your existing dbt project repository into the Mage Pro project directory.
    This ensures all models, macros, seeds, and configuration files are present.
    """

    # Define the URL of your dbt project repository
    dbt_repo_url = "https://github.com/your-org/your-dbt-repo.git"

    # Define the target directory within the Mage project
    target_dir = os.path.join(os.getcwd(), "dbt")

    # Check if the directory already exists to avoid re-cloning
    if os.path.exists(target_dir):
        print(f"Directory {target_dir} already exists. Skipping clone.")
        return

    # Clone the repository into the target directory
    try:
        subprocess.run(
            ["git", "clone", dbt_repo_url, "dbt"],
            check=True,
            cwd=os.getcwd(),
        )
        print(f"Successfully cloned dbt repo into {target_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repo: {e}")
