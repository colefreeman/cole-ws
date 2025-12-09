import requests


@custom
def main(ssh_public_key: str, *args, **kwargs):
    """
    Adds the provided SSH public key to the user's GitHub account as a deploy key.
    This allows subsequent Git operations to authenticate via SSH.
    """

    # Retrieve GitHub personal access token from secrets manager
    github_token: str = get_secret_value("GITHUB_PERSONAL_ACCESS_TOKEN")

    # GitHub API endpoint for user deploy keys
    api_url: str = "https://api.github.com/user/keys"

    # Prepare the request headers with authorization
    headers: dict = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Prepare the payload with the SSH public key
    payload: dict = {
        "title": "Mage Pro SSH Key",
        "key": ssh_public_key,
    }

    # Send POST request to add the SSH key
    response: requests.Response = requests.post(api_url, headers=headers, json=payload)

    # Check response status
    if response.status_code == 201:
        print("Successfully added SSH public key to GitHub.")
    else:
        raise Exception(
            f"Failed to add SSH key: {response.status_code} - {response.text}"
        )
