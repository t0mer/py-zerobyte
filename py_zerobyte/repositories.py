"""Repositories API methods."""

from typing import Dict, Any, List


class RepositoriesAPI:
    """Repositories API methods."""

    def __init__(self, client):
        """Initialize RepositoriesAPI with client instance."""
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all repositories.

        Returns:
            list: List of repositories

        Example:
            >>> repositories = client.repositories.list()
            >>> for repo in repositories:
            ...     print(repo['name'])
        """
        return self.client._make_request("GET", "/api/v1/repositories")

    def create(self, repository_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new repository.

        Args:
            repository_data: Repository configuration including:
                - name (str): Repository name
                - config (dict): Backend-specific configuration with a 'backend' key
                  ('local', 'sftp', 's3', 'r2', 'azure', 'gcs', 'rest', 'rclone')
                - compressionMode (str, optional): 'auto', 'max', or 'off'

        Returns:
            dict: Created repository information

        Example:
            >>> repo = client.repositories.create({
            ...     "name": "my-backup-repo",
            ...     "compressionMode": "auto",
            ...     "config": {
            ...         "backend": "local",
            ...         "path": "/backups/repo1"
            ...     }
            ... })
        """
        return self.client._make_request(
            "POST",
            "/api/v1/repositories",
            data=repository_data
        )

    def get(self, name: str) -> Dict[str, Any]:
        """
        Get a specific repository by shortId.

        Args:
            name: Repository shortId (e.g., "Eilm20ua")

        Returns:
            dict: Repository information

        Example:
            >>> repo = client.repositories.get("Eilm20ua")
            >>> print(repo['name'])
        """
        return self.client._make_request(
            "GET",
            f"/api/v1/repositories/{name}"
        )

    def update(self, name: str, repository_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a repository.

        Args:
            name: Repository shortId
            repository_data: Updated repository configuration

        Returns:
            dict: Updated repository information

        Example:
            >>> repo = client.repositories.update(
            ...     "Eilm20ua",
            ...     {"compressionMode": "max"}
            ... )
        """
        return self.client._make_request(
            "PATCH",
            f"/api/v1/repositories/{name}",
            data=repository_data
        )

    def delete(self, name: str) -> Dict[str, Any]:
        """
        Delete a repository.

        Args:
            name: Repository shortId

        Returns:
            dict: Deletion response

        Example:
            >>> response = client.repositories.delete("Eilm20ua")
        """
        return self.client._make_request(
            "DELETE",
            f"/api/v1/repositories/{name}"
        )

    def doctor(self, name: str) -> Dict[str, Any]:
        """
        Run doctor command on a repository to check and repair issues.

        Args:
            name: Repository shortId

        Returns:
            dict: Doctor command result

        Example:
            >>> result = client.repositories.doctor("Eilm20ua")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/repositories/{name}/doctor"
        )

    def list_rclone_remotes(self) -> List[str]:
        """
        List available rclone remotes.

        Returns:
            list: List of rclone remote names

        Example:
            >>> remotes = client.repositories.list_rclone_remotes()
        """
        return self.client._make_request("GET", "/api/v1/repositories/rclone-remotes")
