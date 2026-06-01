"""Backup Schedules API methods."""

from typing import Dict, Any, List, Optional


class BackupSchedulesAPI:
    """Backup Schedules API methods."""

    def __init__(self, client):
        """Initialize BackupSchedulesAPI with client instance."""
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all backup schedules.

        Returns:
            list: List of backup schedules

        Example:
            >>> schedules = client.backup_schedules.list()
            >>> for schedule in schedules:
            ...     print(f"{schedule['name']}: {schedule['cronExpression']}")
        """
        return self.client._make_request("GET", "/api/v1/backups")

    def create(self, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new backup schedule.

        Args:
            schedule_data: Schedule configuration including:
                - name (str): Schedule name (1-32 characters)
                - repositoryId (str): Target repository shortId
                - volumeId (int): Source volume ID
                - cronExpression (str): Cron expression for schedule timing
                - enabled (bool): Whether schedule is enabled
                - backupPaths (list): Paths to back up
                - excludePatterns (list): Glob patterns to exclude (optional)
                - excludeIfPresent (list): Exclude dirs containing these files (optional)
                - retention (dict): Retention policy (optional)
                - tags (list): Tags for the backup (optional)

        Returns:
            dict: Created backup schedule

        Example:
            >>> schedule = client.backup_schedules.create({
            ...     "name": "Daily Backup",
            ...     "repositoryId": "Eilm20ua",
            ...     "volumeId": 1,
            ...     "cronExpression": "0 2 * * *",
            ...     "enabled": True,
            ...     "backupPaths": ["/data"],
            ...     "retention": {
            ...         "keepLast": 7,
            ...         "keepDaily": 7,
            ...         "keepWeekly": 4,
            ...         "keepMonthly": 12
            ...     }
            ... })
        """
        return self.client._make_request(
            "POST",
            "/api/v1/backups",
            data=schedule_data
        )

    def get(self, schedule_id: str) -> Dict[str, Any]:
        """
        Get a specific backup schedule.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Backup schedule details

        Example:
            >>> schedule = client.backup_schedules.get("schedule-id")
        """
        return self.client._make_request(
            "GET",
            f"/api/v1/backups/{schedule_id}"
        )

    def update(self, schedule_id: str, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a backup schedule.

        Args:
            schedule_id: Schedule ID
            schedule_data: Updated schedule configuration

        Returns:
            dict: Updated backup schedule

        Example:
            >>> schedule = client.backup_schedules.update(
            ...     "schedule-id",
            ...     {"enabled": False}
            ... )
        """
        return self.client._make_request(
            "PATCH",
            f"/api/v1/backups/{schedule_id}",
            data=schedule_data
        )

    def delete(self, schedule_id: str) -> Dict[str, Any]:
        """
        Delete a backup schedule.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Deletion response

        Example:
            >>> response = client.backup_schedules.delete("schedule-id")
        """
        return self.client._make_request(
            "DELETE",
            f"/api/v1/backups/{schedule_id}"
        )

    def get_for_volume(self, volume_id: int) -> List[Dict[str, Any]]:
        """
        Get all backup schedules for a specific volume.

        Args:
            volume_id: Volume ID

        Returns:
            list: List of backup schedules for the volume

        Example:
            >>> schedules = client.backup_schedules.get_for_volume(1)
        """
        return self.client._make_request(
            "GET",
            f"/api/v1/backups/volume/{volume_id}"
        )

    def run_now(self, schedule_id: str) -> Dict[str, Any]:
        """
        Run a backup schedule immediately.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Backup execution response

        Example:
            >>> response = client.backup_schedules.run_now("schedule-id")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/backups/{schedule_id}/run"
        )

    def stop_backup(self, schedule_id: str) -> Dict[str, Any]:
        """
        Stop a running backup.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Stop response

        Example:
            >>> response = client.backup_schedules.stop_backup("schedule-id")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/backups/{schedule_id}/stop"
        )

    def run_forget(self, schedule_id: str) -> Dict[str, Any]:
        """
        Run the forget command to apply retention policy.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Forget command response

        Example:
            >>> response = client.backup_schedules.run_forget("schedule-id")
        """
        return self.client._make_request(
            "POST",
            f"/api/v1/backups/{schedule_id}/forget"
        )

    def get_notifications(self, schedule_id: str) -> Dict[str, Any]:
        """
        Get notification settings for a backup schedule.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Notification settings

        Example:
            >>> notifications = client.backup_schedules.get_notifications("schedule-id")
        """
        return self.client._make_request(
            "GET",
            f"/api/v1/backups/{schedule_id}/notifications"
        )

    def update_notifications(
        self,
        schedule_id: str,
        notifications_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update notification settings for a backup schedule.

        Args:
            schedule_id: Schedule ID
            notifications_data: Notification configuration

        Returns:
            dict: Updated notification settings

        Example:
            >>> notifications = client.backup_schedules.update_notifications(
            ...     "schedule-id",
            ...     {"onSuccess": True, "onFailure": True, "destinations": [1, 2]}
            ... )
        """
        return self.client._make_request(
            "PUT",
            f"/api/v1/backups/{schedule_id}/notifications",
            data=notifications_data
        )

    def get_mirrors(self, schedule_id: str) -> Dict[str, Any]:
        """
        Get mirror settings for a backup schedule.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Mirror settings

        Example:
            >>> mirrors = client.backup_schedules.get_mirrors("schedule-id")
        """
        return self.client._make_request(
            "GET",
            f"/api/v1/backups/{schedule_id}/mirrors"
        )

    def update_mirrors(
        self,
        schedule_id: str,
        mirrors_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update mirror settings for a backup schedule.

        Args:
            schedule_id: Schedule ID
            mirrors_data: Mirror configuration

        Returns:
            dict: Updated mirror settings

        Example:
            >>> mirrors = client.backup_schedules.update_mirrors(
            ...     "schedule-id",
            ...     {"enabled": True, "repositories": ["repo-id-1", "repo-id-2"]}
            ... )
        """
        return self.client._make_request(
            "PUT",
            f"/api/v1/backups/{schedule_id}/mirrors",
            data=mirrors_data
        )

    def get_mirror_compatibility(self, schedule_id: str) -> Dict[str, Any]:
        """
        Check mirror compatibility for a backup schedule.

        Args:
            schedule_id: Schedule ID

        Returns:
            dict: Mirror compatibility information

        Example:
            >>> compatibility = client.backup_schedules.get_mirror_compatibility("schedule-id")
        """
        return self.client._make_request(
            "GET",
            f"/api/v1/backups/{schedule_id}/mirrors/compatibility"
        )

    def reorder(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reorder backup schedules.

        Args:
            order_data: New order configuration with schedule IDs

        Returns:
            dict: Reorder response

        Example:
            >>> response = client.backup_schedules.reorder(
            ...     {"scheduleIds": ["id-3", "id-1", "id-2"]}
            ... )
        """
        return self.client._make_request(
            "POST",
            "/api/v1/backups/reorder",
            data=order_data
        )
