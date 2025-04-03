import base64
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict

import requests


class HandleRepository:
    """Class to handle GitHub repository by API rest"""

    def __init__(self, username, token) -> None:
        """Initialize the repository handler.

        Args:
            username (str): GitHub username
            token (str): GitHub API token
        """
        self._username = username
        self._api_base_url = 'https://api.github.com'
        self._headers = {
            'Authorization': f'Bearer {token}',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def create_repo(
            self, repo_name: str, repo_description: str,
            private: bool = True) -> Dict[str, Any]:
        """Create a new GitHub repository.

        Args:
            repo_name (str): Name of the repository
            repo_description (str): Description of the repository
            private (bool): Whether the repository should be private
                (default: True)
        """
        if not repo_name or not repo_name.strip():
            raise ValueError("Repository name cannot be blank")

        url = f'{self._api_base_url}/user/repos'

        data = {
            'name': repo_name.strip(),
            'description': repo_description,
            'private': private
        }

        try:
            resp = requests.post(
                url=url, headers=self._headers, json=data, timeout=10)
            resp.raise_for_status()

            if resp.status_code == HTTPStatus.CREATED:
                return resp.json()

            else:
                raise requests.RequestException(
                    f'Failed to create repository. Status: {resp.status_code}')

        except requests.RequestException as e:
            raise requests.RequestException(
                f'Error creating repository: {str(e)}') from e

    def encode_file_content(self, path: str) -> bytes:
        """Encode a file's content to base64.

        Args:
            path (str): Path to the file to be encoded

        Returns:
            bytes: Base64 encoded content of the file

        Raises:
            FileNotFoundError: If the specified file does not exists
            IOError: If there are problems reading the file
        """

        try:
            with open(path, 'rb') as f:
                file_content = f.read()
            return base64.b64encode(file_content)

        except FileNotFoundError:
            raise FileNotFoundError(f'File not found at path: {path}')

        except IOError as e:
            raise IOError(f'Error reading file at {path}: {str(e)}')

    def add_file(self, repo_name: str, path: str, msg: str) -> Dict[str, Any]:
        """Add a file to GitHub repository.

        Args:
            repo_name (str): Name of the repository where the file will be add
            path (str): Path of the file to be added
            msg (str): Commit message for the file addition

        Returns:
            Dict[str, Any]: Response data from GitHub API

        Raises:
            ValueError: If any of the input paramters are empty or invalid
            requests.RequestException: If the API request somehow fails
            FileNotFoundError: If the file path specified does not exist
            IOError: If there are problems reading the file
        """
        if not repo_name or not repo_name.strip():
            raise ValueError("Repository name cannot be blank")

        if not msg or not msg.strip():
            raise ValueError("Commit message cannot be blank")

        try:
            encoded_file = self.encode_file_content(path=path)
            file_name = Path(path).name

            url_file = (
                (
                    f'{self._api_base_url}/repos/{self._username}/'
                    f'{repo_name}/contents/{file_name}'
                )
            )

            data = {
                'message': msg,
                'content': encoded_file.decode('utf-8')
            }

            resp = requests.put(url=url_file, json=data,
                                headers=self._headers, timeout=10)
            resp.raise_for_status()

            return resp.json()

        except requests.RequestException as e:
            raise requests.RequestException(
                f'Failed to add file to repository: {str(e)}')
