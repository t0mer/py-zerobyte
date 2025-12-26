# Zerobyte SDK API Reference

Complete API reference for the Zerobyte SDK.

## Table of Contents

- [Client](#client)
- [Authentication API](#authentication-api)
- [Volumes API](#volumes-api)
- [Repositories API](#repositories-api)
- [Snapshots API](#snapshots-api)
- [Backup Schedules API](#backup-schedules-api)
- [Notifications API](#notifications-api)
- [System API](#system-api)
- [Exceptions](#exceptions)

## Client

### ZerobyteClient

Main client for interacting with the Zerobyte API.

**Constructor:**
```python
ZerobyteClient(url, username, password, auto_login=True)
```

**Parameters:**
- `url` (str): Base URL of the Zerobyte API
- `username` (str): Username for authentication
- `password` (str): Password for authentication
- `auto_login` (bool): Whether to automatically login on initialization (default: True)

**Properties:**
- `auth`: Authentication API methods
- `volumes`: Volumes API methods
- `repositories`: Repositories API methods
- `snapshots`: Snapshots API methods
- `backup_schedules`: Backup Schedules API methods
- `notifications`: Notifications API methods
- `system`: System API methods

---

## Authentication API

Access via `client.auth`

### register(username, password)
Register a new user.

**Returns:** dict - Registration response with user information

### login(username, password)
Login with username and password.

**Returns:** dict - Login response with user information

### logout()
Logout current user.

**Returns:** dict - Logout response

### get_me()
Get current authenticated user information.

**Returns:** dict - Current user information

### get_status()
Get authentication system status.

**Returns:** dict - Authentication system status (e.g., hasUsers)

### change_password(current_password, new_password)
Change current user password.

**Returns:** dict - Password change response

---

## Volumes API

Access via `client.volumes`

### list()
List all volumes.

**Returns:** list - List of volumes

### create(volume_data)
Create a new volume.

**Parameters:**
- `volume_data` (dict): Volume configuration
  - `name` (str): Volume name
  - `device` (str): Device path
  - `mountPoint` (str): Mount point path
  - `filesystem` (str): Filesystem type
  - `autoRemount` (bool): Auto remount on startup
  - `readonly` (bool): Mount as readonly
  - `options` (list): Mount options

**Returns:** dict - Created volume information

### test_connection(volume_data)
Test connection to a volume before creating it.

**Returns:** dict - Test result

### get(volume_id)
Get a specific volume by ID.

**Returns:** dict - Volume information

### update(volume_id, volume_data)
Update a volume.

**Returns:** dict - Updated volume information

### delete(volume_id)
Delete a volume.

**Returns:** dict - Deletion response

### mount(volume_id)
Mount a volume.

**Returns:** dict - Mount response

### unmount(volume_id)
Unmount a volume.

**Returns:** dict - Unmount response

### health_check(volume_id)
Perform health check on a volume.

**Returns:** dict - Health check result

### list_files(volume_id, path=None)
List files in a volume.

**Parameters:**
- `path` (str, optional): Path within the volume

**Returns:** dict - File listing

### browse_filesystem(path=None)
Browse the filesystem.

**Parameters:**
- `path` (str, optional): Filesystem path

**Returns:** dict - Directory listing

### list_rclone_remotes()
List available rclone remotes.

**Returns:** list - List of rclone remote names

---

## Repositories API

Access via `client.repositories`

### list(volume_id)
List all repositories for a volume.

**Returns:** list - List of repositories

### create(volume_id, repository_data)
Create a new repository in a volume.

**Parameters:**
- `repository_data` (dict): Repository configuration
  - `name` (str): Repository name
  - `type` (str): Repository type
  - `config` (dict): Type-specific configuration
  - `password` (str, optional): Repository password

**Returns:** dict - Created repository information

### get(volume_id, repository_id)
Get a specific repository.

**Returns:** dict - Repository information

### update(volume_id, repository_id, repository_data)
Update a repository.

**Returns:** dict - Updated repository information

### delete(volume_id, repository_id)
Delete a repository.

**Returns:** dict - Deletion response

### doctor(volume_id, repository_id)
Run doctor command on a repository to check and repair issues.

**Returns:** dict - Doctor command result

---

## Snapshots API

Access via `client.snapshots`

### list(volume_id, repository_id)
List all snapshots in a repository.

**Returns:** list - List of snapshots

### get_details(volume_id, repository_id, snapshot_id)
Get details of a specific snapshot.

**Returns:** dict - Snapshot details

### delete(volume_id, repository_id, snapshot_id)
Delete a snapshot.

**Returns:** dict - Deletion response

### list_files(volume_id, repository_id, snapshot_id, path=None)
List files in a snapshot.

**Parameters:**
- `path` (str, optional): Path within snapshot

**Returns:** dict - File listing

### restore(volume_id, repository_id, snapshot_id, restore_data)
Restore a snapshot.

**Parameters:**
- `restore_data` (dict): Restore configuration
  - `target` (str): Target path for restoration
  - `include` (list, optional): Paths to include
  - `exclude` (list, optional): Paths to exclude

**Returns:** dict - Restore response

---

## Backup Schedules API

Access via `client.backup_schedules`

### list(volume_id, repository_id)
List all backup schedules for a repository.

**Returns:** list - List of backup schedules

### create(volume_id, repository_id, schedule_data)
Create a new backup schedule.

**Parameters:**
- `schedule_data` (dict): Schedule configuration
  - `name` (str): Schedule name
  - `schedule` (str): Cron expression
  - `enabled` (bool): Whether schedule is enabled
  - `backupPaths` (list): Paths to backup
  - `excludePaths` (list, optional): Paths to exclude
  - `retention` (dict, optional): Retention policy
  - `tags` (list, optional): Tags for the backup

**Returns:** dict - Created backup schedule

### get(volume_id, repository_id, schedule_id)
Get a specific backup schedule.

**Returns:** dict - Backup schedule details

### update(volume_id, repository_id, schedule_id, schedule_data)
Update a backup schedule.

**Returns:** dict - Updated backup schedule

### delete(volume_id, repository_id, schedule_id)
Delete a backup schedule.

**Returns:** dict - Deletion response

### get_for_volume(volume_id)
Get all backup schedules for a volume across all repositories.

**Returns:** list - List of backup schedules

### run_now(volume_id, repository_id, schedule_id)
Run a backup schedule immediately.

**Returns:** dict - Backup execution response

### stop_backup(volume_id, repository_id, schedule_id)
Stop a running backup.

**Returns:** dict - Stop response

### run_forget(volume_id, repository_id, schedule_id)
Run the forget command to apply retention policy.

**Returns:** dict - Forget command response

### get_notifications(volume_id, repository_id, schedule_id)
Get notification settings for a backup schedule.

**Returns:** dict - Notification settings

### update_notifications(volume_id, repository_id, schedule_id, notifications_data)
Update notification settings for a backup schedule.

**Returns:** dict - Updated notification settings

### get_mirrors(volume_id, repository_id, schedule_id)
Get mirror settings for a backup schedule.

**Returns:** dict - Mirror settings

### update_mirrors(volume_id, repository_id, schedule_id, mirrors_data)
Update mirror settings for a backup schedule.

**Returns:** dict - Updated mirror settings

### get_mirror_compatibility(volume_id, repository_id, schedule_id)
Check mirror compatibility for a backup schedule.

**Returns:** dict - Mirror compatibility information

### reorder(volume_id, repository_id, order_data)
Reorder backup schedules.

**Parameters:**
- `order_data` (dict): New order configuration
  - `scheduleIds` (list): Ordered list of schedule IDs

**Returns:** dict - Reorder response

---

## Notifications API

Access via `client.notifications`

### list_destinations()
List all notification destinations.

**Returns:** list - List of notification destinations

### create_destination(destination_data)
Create a new notification destination.

**Parameters:**
- `destination_data` (dict): Destination configuration
  - `name` (str): Destination name
  - `type` (str): Destination type (email, slack, webhook, etc.)
  - `config` (dict): Type-specific configuration

**Returns:** dict - Created notification destination

### get_destination(destination_id)
Get a specific notification destination.

**Returns:** dict - Notification destination details

### update_destination(destination_id, destination_data)
Update a notification destination.

**Returns:** dict - Updated notification destination

### delete_destination(destination_id)
Delete a notification destination.

**Returns:** dict - Deletion response

### test_destination(destination_id)
Test a notification destination.

**Returns:** dict - Test result

---

## System API

Access via `client.system`

### get_info()
Get system information.

**Returns:** dict - System information including version, platform, etc.

### download_restic_password()
Download the Restic password file.

**Returns:** str - Restic password content

---

## Exceptions

### ZerobyteError
Base exception for all Zerobyte SDK errors.

### AuthenticationError
Raised when authentication fails.

**Inherits from:** ZerobyteError

### APIError
Raised when the API returns an error.

**Inherits from:** ZerobyteError

**Attributes:**
- `status_code` (int): HTTP status code
- `response`: Raw response object

### NotFoundError
Raised when a resource is not found (404).

**Inherits from:** APIError

### ValidationError
Raised when request validation fails.

**Inherits from:** APIError

---

## Error Handling Example

```python
from py_zerobyte import (
    ZerobyteClient,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    APIError
)

try:
    client = ZerobyteClient(
        url="http://localhost:4096",
        username="admin",
        password="password"
    )
    
    volume = client.volumes.get(999)
    
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except NotFoundError as e:
    print(f"Not found: {e} (status: {e.status_code})")
except ValidationError as e:
    print(f"Validation error: {e}")
except APIError as e:
    print(f"API error: {e} (status: {e.status_code})")
```
