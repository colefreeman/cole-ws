import os
import subprocess


@custom
def configure_git_to_use_ssh_key(*args, **kwargs):
    """
    Configures Git to use the generated SSH private key for authentication.
    Sets the GIT_SSH_COMMAND environment variable to specify the SSH key file.
    """

    # Path to the SSH private key generated earlier
    ssh_key_path = "/home/src/coles-workspace-2/.ssh/id_ed25519"

    # Ensure the SSH key file exists
    if not os.path.exists(ssh_key_path):
        raise FileNotFoundError(f"SSH key not found at {ssh_key_path}")

    # Set the GIT_SSH_COMMAND environment variable to specify the SSH key
    git_ssh_command = f"ssh -i {ssh_key_path} -o IdentitiesOnly=yes"

    # Set the environment variable for the current process
    os.environ["GIT_SSH_COMMAND"] = git_ssh_command

    # Optionally, verify the configuration by running a git command
    try:
        subprocess.run(
            ["git", "config", "--global", "core.sshCommand", git_ssh_command],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to set git ssh command") from e
