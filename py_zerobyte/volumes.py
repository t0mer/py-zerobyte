"""Volumes API methods."""

from typing import Dict, Any, List, Optional


class VolumesAPI:
    """Volumes API methods."""

    def __init__(self, client):
        """Initialize VolumesAPI with client instance."""
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all volumes.

        Returns:
            list: List of volumes

        Example:
            >>> volumes = client.volumes.list()
            >>> for volume in volumes:
            ...     print(volume['name'])
        """
        return self.client._make_request("GET", "/api/v1/volumes")

    def create(self, volume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new volume.

        Args:
            volume_data: Volume configuration including:
                - autoRemount (bool): Auto remount on system startup
                - config (dict): Backend-specific configuration with a 'backend' key
                - name (str): Volume name

        Returns:
            dict: Created volume information

        Example:
            >>> volume = client.volumes.create({
            ...     "name": "my-backup",
            ...     "autoRemount": True,
            ...     "config": {
            ...         "backend": "directory",
            ...         "path": "/mnt/backup"
            ...     }
            ... })
        """
        return self.client._make_request(
            "POST",
            "/api/v1/volumes",
            data=volume_data
        )

    def test_connection(self, volume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test connection to a volume before creating it.

        Args:
            volume_data: Volume configuration to test

        Returns:
            dict: Test result

        Example:
            >>> result = client.volumes.test_connection({
            ...     "config": {"backend": "directory", "path": "/mnt/backup"}
            ... })
        """
        return self.client._make_request(
            "POST",
            "/api/v1/volumes/test-connection",
            data=volume_data
        )

    def get(self, volume_name: str) -> Dict[str, Any]:
        """
        Get a specific volume by its shortId or name.

        Args:
            volume_name: Volume shortId (e.g., "0-b-U31s")

        Returns:
            dict: Volume information

        Example:
            >>> volume = client.volumes.get("0-b-U31s")
            >>> print(volume['name'])
        """
        return self.client._make_request("GET", f"/api/v1/volumes/{volume_name}")

    def update(self, volume_name: str, volume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a volume.

        Args:
            volume_name: Volume shortId
            volume_data: Updated volume configuration

        Returns:
            dict: Updated volume information

        Example:
            >>> volume = client.volumes.update("0-b-U31s", {
            ...     "name": "updated-name",
            ...     "autoRemount": True
            ... })
        """
        return self.client._make_request(
            "PUT",
            f"/api/v1/volumes/{volume_name}",
            data=volume_data
        )

    def delete(self, volume_name: str) -> Dict[str, Any]:
        """
        Delete a volume.

        Args:
            volume_name: Volume shortId

        Returns:
            dict: Deletion response

        Example:
            >>> response = client.volumes.delete("0-b-U31s")
        """
        return self.client._make_request("DELETE", f"/api/v1/volumes/{volume_name}")

    def mount(self, volume_name: str) -> Dict[str, Any]:
        """
        Mount a volume.

        Args:
            volume_name: Volume shortId

        Returns:
            dict: Mount response

        Example:
            >>> response = client.volumes.mount("0-b-U31s")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/volumes/{volume_name}/mount"
        )

    def unmount(self, volume_name: str) -> Dict[str, Any]:
        """
        Unmount a volume.

        Args:
            volume_name: Volume shortId

        Returns:
            dict: Unmount response

        Example:
            >>> response = client.volumes.unmount("0-b-U31s")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/volumes/{volume_name}/unmount"
        )

    def health_check(self, volume_name: str) -> Dict[str, Any]:
        """
        Perform health check on a volume.

        Args:
            volume_name: Volume shortId

        Returns:
            dict: Health check result

        Example:
            >>> health = client.volumes.health_check("0-b-U31s")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/volumes/{volume_name}/health-check"
        )

    def list_files(self, volume_name: str, path: Optional[str] = None) -> Dict[str, Any]:
        """
        List files in a volume.

        Args:
            volume_name: Volume shortId
            path: Path within the volume (optional)

        Returns:
            dict: File listing

        Example:
            >>> files = client.volumes.list_files("0-b-U31s", path="/backups")
        """
        params = {}
        if path:
            params['path'] = path

        return self.client._make_request(
            "GET",
            f"/api/v1/volumes/{volume_name}/files",
            params=params
        )

    def browse_filesystem(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Browse the server filesystem.

        Args:
            path: Filesystem path to browse (absolute, defaults to /)

        Returns:
            dict: Directory listing

        Example:
            >>> listing = client.volumes.browse_filesystem(path="/mnt")
        """
        params = {}
        if path:
            params['path'] = path

        return self.client._make_request(
            "GET",
            "/api/v1/volumes/filesystem/browse",
            params=params
        )
