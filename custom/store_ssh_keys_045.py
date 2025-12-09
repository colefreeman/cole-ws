from mage_ai.data_preparation.shared.secrets import create_secret


@custom
def store_ssh_keys(private_key_path: str, *args, **kwargs):
    """
    Store SSH private and public keys securely in secrets manager.

    Args:
        private_key_path (str): Path to the SSH private key file.
        public_key_path (str): Path to the SSH public key file.
        secrets_manager_key_private (str): Secret name/key for private key storage.
        secrets_manager_key_public (str): Secret name/key for public key storage.
        **kwargs: Additional arguments.
    """

    public_key_path: str = None
    secrets_manager_key_private: str = None
    secrets_manager_key_public: str = None

    # Read the SSH private key from the specified file path
    with open(private_key_path, "r") as private_file:
        private_key_data = private_file.read()

    # Read the SSH public key from the specified file path
    with open(public_key_path, "r") as public_file:
        public_key_data = public_file.read()

    # Store the private key securely
    create_secret(
        key=secrets_manager_key_private,
        value=private_key_data,
    )

    # Store the public key securely
    create_secret(
        key=secrets_manager_key_public,
        value=public_key_data,
    )
