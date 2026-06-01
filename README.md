# Zerobyte SDK

A Python SDK for the [Zerobyte](https://github.com/t0mer/py-zerobyte) backup API — manage volumes, repositories, snapshots, backup schedules, and notifications from Python.

## Installation

```bash
pip install py-zerobyte
```

Or install from source:

```bash
git clone https://github.com/t0mer/py-zerobyte.git
cd py-zerobyte
pip install -e .
```

## Quick Start

```python
from py_zerobyte import ZerobyteClient

client = ZerobyteClient(
    url="http://localhost:4096",
    username="admin",
    password="your-password"
)

# Auto-login runs on init — you're ready to go
session = client.auth.get_me()
print(f"Logged in as: {session['user']['username']}")

volumes = client.volumes.list()
for v in volumes:
    print(f"Volume: {v['name']}  shortId: {v['shortId']}")
```

## Features

- **Authentication** — login, logout, password change via `better-auth`
- **Volumes** — create, update, delete, mount/unmount, health check, file browse
- **Repositories** — manage restic backup repositories (local, S3, R2, SFTP, rclone, …)
- **Snapshots** — list, inspect, browse files, restore, delete
- **Backup Schedules** — cron-driven schedules with retention, mirrors, notifications
- **Notification Destinations** — Telegram, email, Pushover, ntfy, Discord, Slack, webhook
- **System** — capabilities info, restic password retrieval

## Configuration

```python
client = ZerobyteClient(
    url="http://localhost:4096",   # Zerobyte server URL
    username="admin",              # Login username
    password="your-password",      # Login password
    auto_login=True                # Default: True — logs in during __init__
)

# Manual login (when auto_login=False)
client = ZerobyteClient(url=..., username=..., password=..., auto_login=False)
client.login()
```

## Resource IDs

Zerobyte identifies most resources by a **shortId** string (e.g. `"0-b-U31s"`, `"Eilm20ua"`), not by a sequential integer. Always use the `shortId` field from list/create responses when calling get/update/delete methods.

```python
volumes = client.volumes.list()
vol_id = volumes[0]['shortId']   # e.g. "0-b-U31s"
detail  = client.volumes.get(vol_id)
```

---

## Usage Examples

### Authentication

```python
# Check whether any users exist (first-time setup)
status = client.auth.get_status()
if not status['hasUsers']:
    client.auth.register("admin", "initial-password")

# Get current session / user info
session = client.auth.get_me()
print(session['user']['username'])

# Change password
client.auth.change_password("old-password", "new-password")

# Logout
client.auth.logout()
```

### Volumes

```python
# List all volumes
volumes = client.volumes.list()

# Create a volume (directory backend)
volume = client.volumes.create({
    "name": "my-backup",
    "autoRemount": True,
    "config": {
        "backend": "directory",
        "path": "/mnt/backup"
    }
})
vid = volume['shortId']

# Get, update, delete
detail  = client.volumes.get(vid)
updated = client.volumes.update(vid, {"autoRemount": False})
client.volumes.delete(vid)

# Mount / unmount / health check
client.volumes.mount(vid)
client.volumes.unmount(vid)
health = client.volumes.health_check(vid)

# Browse files
files   = client.volumes.list_files(vid, path="/data")
listing = client.volumes.browse_filesystem(path="/mnt")
```

### Repositories

```python
# List all repositories
repos = client.repositories.list()

# Create a local repository
repo = client.repositories.create({
    "name": "local-repo",
    "compressionMode": "auto",
    "config": {
        "backend": "local",
        "path": "/backups/repo1"
    }
})
rid = repo['shortId']

# Get, update (PATCH), delete
detail  = client.repositories.get(rid)
updated = client.repositories.update(rid, {"compressionMode": "max"})
client.repositories.delete(rid)

# Doctor (check + repair)
result = client.repositories.doctor(rid)

# List available rclone remotes
remotes = client.repositories.list_rclone_remotes()
```

### Snapshots

```python
# List snapshots for a repository (use repository shortId)
snapshots = client.snapshots.list(repository_name=rid)

if snapshots:
    snap_id = snapshots[0]['id']

    # Get snapshot detail
    detail = client.snapshots.get_details(rid, snap_id)

    # Browse files inside a snapshot
    files = client.snapshots.list_files(rid, snap_id, path="/home")

    # Restore
    client.snapshots.restore(rid, {
        "target": "/restore/path",
        "snapshotId": snap_id,
        "include": ["/home/user"],
        "exclude": ["/home/user/.cache"]
    })

    # Delete a snapshot
    client.snapshots.delete(rid, snap_id)
```

### Backup Schedules

```python
# List all schedules
schedules = client.backup_schedules.list()

# Create a schedule
schedule = client.backup_schedules.create({
    "name": "Daily Backup",
    "repositoryId": rid,         # repository shortId
    "volumeId": 1,               # volume numeric id
    "cronExpression": "0 2 * * *",
    "enabled": True,
    "backupPaths": ["/home", "/etc"],
    "excludePatterns": ["**/.cache/**"],
    "retentionPolicy": {
        "keepLast": 7,
        "keepDaily": 7,
        "keepWeekly": 4,
        "keepMonthly": 12
    },
    "tags": ["daily", "production"]
})
sched_id = schedule['shortId']

# Get, update, delete
detail  = client.backup_schedules.get(sched_id)
updated = client.backup_schedules.update(sched_id, {
    "repositoryId": rid,
    "cronExpression": "0 3 * * *",
    "enabled": False
})
client.backup_schedules.delete(sched_id)

# All schedules for one volume
vol_schedules = client.backup_schedules.get_for_volume(volume_id=1)

# Trigger / stop / forget
client.backup_schedules.run_now(sched_id)
client.backup_schedules.stop_backup(sched_id)
client.backup_schedules.run_forget(sched_id)

# Notifications per schedule
client.backup_schedules.update_notifications(sched_id, {
    "onSuccess": True,
    "onFailure": True,
    "destinations": [1, 2]
})

# Mirrors
client.backup_schedules.update_mirrors(sched_id, {
    "enabled": True,
    "repositories": [rid2]
})
compat = client.backup_schedules.get_mirror_compatibility(sched_id)

# Reorder
client.backup_schedules.reorder({"scheduleIds": ["id-c", "id-a", "id-b"]})
```

### Notifications

```python
# List all destinations
destinations = client.notifications.list_destinations()

# Create a Telegram destination
# Note: the destination type lives inside the config dict
dest = client.notifications.create_destination({
    "name": "Telegram Alerts",
    "config": {
        "type": "telegram",
        "botToken": "123456:ABC-DEF",
        "chatId": "-1001234567890"
    }
})
did = dest['id']

# Create an email destination
client.notifications.create_destination({
    "name": "Admin Email",
    "config": {
        "type": "email",
        "from": "backup@example.com",
        "to": ["admin@example.com"],
        "smtpHost": "smtp.gmail.com",
        "smtpPort": 587,
        "useTLS": True
    }
})

# Get, update, delete
detail  = client.notifications.get_destination(did)
updated = client.notifications.update_destination(did, {"name": "Renamed"})
client.notifications.delete_destination(did)

# Send a test message
client.notifications.test_destination(did)
```

### System

```python
# Server capabilities
info = client.system.get_info()
print(info['capabilities'])   # {"rclone": bool, "sysAdmin": bool}

# Retrieve the restic repository password (requires account password for verification)
result = client.system.download_restic_password("your-account-password")
```

---

## Error Handling

```python
from py_zerobyte import (
    ZerobyteClient,
    ZerobyteError,
    AuthenticationError,
    APIError,
    NotFoundError,
    ValidationError,
)

try:
    client = ZerobyteClient(url="http://localhost:4096",
                            username="admin", password="wrong")
except AuthenticationError as e:
    print(f"Login failed: {e}")

try:
    vol = client.volumes.get("non-existent-id")
except NotFoundError as e:
    print(f"Not found (HTTP {e.status_code}): {e}")

try:
    client.volumes.create({})          # missing required fields
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    client.volumes.list()
except APIError as e:
    print(f"API error (HTTP {e.status_code}): {e}")
except ZerobyteError as e:
    print(f"SDK error: {e}")
```

---

## Development

```bash
# Install with dev extras
pip install -e ".[dev]"

# Run tests
pytest

# Format
black py_zerobyte/

# Lint
flake8 py_zerobyte/
```

## License

MIT — see [LICENSE](LICENSE)

## Links

- PyPI: https://pypi.org/project/py-zerobyte/
- Issues: https://github.com/t0mer/py-zerobyte/issues

## Changelog

### 1.2.1
- Migrated auth to `better-auth` endpoints
- Volumes now use `shortId` (string) as identifier in all path parameters
- Repositories `update()` uses PATCH; added `list_rclone_remotes()`
- Backup schedules restructured to flat `/api/v1/backups` API
- Notifications path updated; `update_destination()` uses PATCH
- `system.download_restic_password()` now requires account password

### 1.0.0
- Initial release
