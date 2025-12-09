import os
import subprocess


@data_loader
def generate_ssh_key_pair(*args, **kwargs):
    """
    Generate an SSH key pair using the ed25519 algorithm and associate it with the user's email.
    Save the private key in the ~/.ssh directory and output the public key as a string.
    """

    # Define user email for the SSH key comment
    user_email = "freem111@gmail.com"

    # Define the SSH directory path
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)

    # Define the key file paths
    private_key_path = os.path.join(ssh_dir, "id_ed25519")
    public_key_path = f"{private_key_path}.pub"

    # Generate the SSH key pair using ssh-keygen
    subprocess.run(
        [
            "ssh-keygen",
            "-t",
            "ed25519",
            "-C",
            user_email,
            "-f",
            private_key_path,
            "-N",
            "",  # No passphrase
        ],
        check=True,
    )

    # Read the public key content
    with open(public_key_path, "r") as pub_key_file:
        public_key = pub_key_file.read().strip()

    # Return the public key string
    return public_key
