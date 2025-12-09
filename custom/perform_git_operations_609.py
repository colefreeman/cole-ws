import subprocess


@custom
def perform_git_operations(git_command: str, *args, **kwargs):
    """
    Perform Git operations (commit, push, pull, etc.) using SSH key authentication.

    Args:
        git_command (str): The Git command to execute, e.g., 'commit', 'push', 'pull'.
        branch_name (str): The branch to operate on, default is 'main'.
        commit_message (str): The commit message for 'commit' command.
    """

    branch_name: str = "main"
    commit_message: str = "Update"

    # Construct the Git command based on input
    if git_command == "commit":
        cmd = ["git", "commit", "-m", commit_message]
    elif git_command == "push":
        cmd = ["git", "push", "origin", branch_name]
    elif git_command == "pull":
        cmd = ["git", "pull", "origin", branch_name]
    elif git_command == "checkout":
        cmd = ["git", "checkout", branch_name]
    elif git_command == "add":
        cmd = ["git", "add", "."]
    else:
        raise ValueError(f"Unsupported git command: {git_command}")

    # Set environment variable for SSH to ensure SSH key is used
    env = kwargs.get("env", {}).copy()
    # Assuming SSH key is already configured in the environment
    # or SSH agent is running with the correct key

    # Execute the command
    try:
        subprocess.run(cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command '{git_command}' failed: {e}")

    # Optional: Return success status or logs
