from typing import Any, Dict, List

import pandas as pd
import requests


class ReposData:
    """Class do handle GitHub repository data fetching"""

    def __init__(self, owner: str, acess_token: str) -> None:
        """Initialize the repository data handler.

        Args:
            owner (str): GitHub username/organization
            acess_token (str): GitHub API token
        """
        self._owner = owner
        self._api_base_url = 'https://api.github.com'
        self._headers = {
            'Authorization': f'Bearer {acess_token}',
            'X-Github-Api-Version': '2022-11-28'
        }
        self._repos_list: List[Dict[str, Any]] | None = None
        self._dataframe: pd.DataFrame | None = None

    @property
    def repos(self) -> List[Dict[str, Any]]:
        """Fetch and cache repository data."""
        if self._repos_list is None:
            repos_list = []
            url = f'{self._api_base_url}/users/{self._owner}/repos'
            page = 1

            try:
                while True:
                    response = requests.get(
                        url=f'{url}?page={page}', headers=self._headers,
                        timeout=10
                    )
                    response.raise_for_status()

                    data = response.json()
                    if not data:
                        break

                    repos_list.extend(data)
                    page += 1

                self._repos_list = repos_list

            except requests.RequestException as e:
                raise Exception(f'Failed to fetch repositories: {str(e)}')

        return self._repos_list

    @property
    def name_repos(self) -> List[str]:
        """Get repository names."""
        return [repo['name'] for repo in self.repos if 'name' in repo]

    @property
    def lang_repos(self) -> List[str]:
        """Get repository primary languages."""
        return [repo['language'] for repo in self.repos if 'language' in repo]

    @property
    def dataframe(self) -> pd.DataFrame:
        """Get repository data as DataFrame"""
        if self._dataframe is None:
            self._dataframe = pd.DataFrame(
                {'name': self.name_repos, 'language': self.lang_repos})
        return self._dataframe

    def save_csv(self, path: str, index: bool = False):
        """
        Save repositories data to CSV file.

        Args:
            path (str): Path to save the CSV file
            index (bool): Whether to include index in CSV
        """
        if not path.endswith('.csv'):
            path = f'{path}.csv'

        self.dataframe.to_csv(path, index=index)
