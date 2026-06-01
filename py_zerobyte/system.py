"""System API methods."""

from typing import Dict, Any


class SystemAPI:
    """System API methods."""

    def __init__(self, client):
        """Initialize SystemAPI with client instance."""
        self.client = client

    def get_info(self) -> Dict[str, Any]:
        """
        Get system information.

        Returns:
            dict: System information including capabilities

        Example:
            >>> info = client.system.get_info()
            >>> print(info['capabilities'])
        """
        return self.client._make_request("GET", "/api/v1/system/info")

    def download_restic_password(self, password: str) -> Dict[str, Any]:
        """
        Generate/retrieve the Restic encryption password.

        Args:
            password: User's current account password (required for verification)

        Returns:
            dict: Restic password response

        Example:
            >>> result = client.system.download_restic_password("mypassword")
        """
        return self.client._make_request(
            "POST",
            "/api/v1/system/restic-password",
            data={"password": password}
        )
