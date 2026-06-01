# Quick Start Guide — Zerobyte SDK

## Install

```bash
pip install py-zerobyte
```

## 30-Second Example

```python
from py_zerobyte import ZerobyteClient

client = ZerobyteClient(
    url="http://localhost:4096",
    username="admin",
    password="your-password"
)

volumes = client.volumes.list()
print(f"Found {len(volumes)} volume(s)")
```

## What's Included

- **50 API endpoints** — full coverage of the Zerobyte REST API
- **7 API modules** — auth, volumes, repositories, snapshots, backup_schedules, notifications, system
- **Custom exceptions** — `AuthenticationError`, `NotFoundError`, `ValidationError`, `APIError`
- **Type hints** — IDE-friendly signatures throughout
- **Session management** — single `requests.Session` with automatic cookie handling

## File Overview

### Core Package (`py_zerobyte/`)

| File | Purpose |
|---|---|
| `client.py` | `ZerobyteClient` — entry point, `_make_request`, auth helpers |
| `auth.py` | Login, logout, get_me, change_password, register, status |
| `volumes.py` | CRUD, mount/unmount, health check, file listing |
| `repositories.py` | CRUD, doctor, rclone remotes |
| `snapshots.py` | List, inspect, restore, delete |
| `backup_schedules.py` | Schedules, run/stop/forget, mirrors, notifications, reorder |
| `notifications.py` | Notification destination CRUD + test |
| `system.py` | System info, restic password |
| `exceptions.py` | Exception hierarchy |

### Documentation

| File | Contents |
|---|---|
| `README.md` | Full usage guide with examples for every API |
| `API_REFERENCE.md` | Method signatures, parameters, return shapes |
| `TUTORIAL.md` | Step-by-step walkthrough (connect → backup → restore) |
| `INSTALL.md` | Installation options and troubleshooting |
| `QUICKSTART.md` | This file |
| `PROJECT_SUMMARY.md` | Architecture and design decisions |
| `CHECKLIST.md` | Pre-publish / release checklist |

### Examples (`examples/`)

| File | Shows |
|---|---|
| `basic_usage.py` | Connect, list resources |
| `create_backup_setup.py` | Full backup infrastructure from scratch |
| `restore_snapshot.py` | Snapshot restore workflow |
| `manage_notifications.py` | Notification destination setup |
| `monitor_status.py` | System status reporting |

## API Coverage

| Module | Methods |
|---|---|
| `client.auth` | `register`, `login`, `logout`, `get_me`, `get_status`, `change_password` |
| `client.volumes` | `list`, `create`, `get`, `update`, `delete`, `mount`, `unmount`, `health_check`, `list_files`, `browse_filesystem`, `test_connection` |
| `client.repositories` | `list`, `create`, `get`, `update`, `delete`, `doctor`, `list_rclone_remotes` |
| `client.snapshots` | `list`, `get_details`, `delete`, `list_files`, `restore` |
| `client.backup_schedules` | `list`, `create`, `get`, `update`, `delete`, `get_for_volume`, `run_now`, `stop_backup`, `run_forget`, `get_notifications`, `update_notifications`, `get_mirrors`, `update_mirrors`, `get_mirror_compatibility`, `reorder` |
| `client.notifications` | `list_destinations`, `create_destination`, `get_destination`, `update_destination`, `delete_destination`, `test_destination` |
| `client.system` | `get_info`, `download_restic_password` |

## Key Concepts

### Resource IDs

Most resources are identified by a **shortId** string (e.g. `"0-b-U31s"`), not a sequential integer. Use the `shortId` field from list/create responses.

```python
repos = client.repositories.list()
rid = repos[0]['shortId']          # "Eilm20ua"
repo = client.repositories.get(rid)
```

### Backup Schedule Creation

`repositoryId` and `volumeId` are **body fields**, not path parameters:

```python
schedule = client.backup_schedules.create({
    "name": "Daily",
    "repositoryId": "Eilm20ua",    # repository shortId
    "volumeId": 1,                 # volume numeric id
    "cronExpression": "0 2 * * *",
    "enabled": True,
    "backupPaths": ["/data"]
})
sched_id = schedule['shortId']
```

### Notification Destination Type

The destination `type` lives **inside** the `config` dict:

```python
client.notifications.create_destination({
    "name": "My Telegram",
    "config": {
        "type": "telegram",
        "botToken": "...",
        "chatId": "..."
    }
})
```

## Common Patterns

```python
# List → act on first result
vols = client.volumes.list()
vid  = vols[0]['shortId']
client.volumes.mount(vid)

# Create schedule, run immediately
sched = client.backup_schedules.create({...})
client.backup_schedules.run_now(sched['shortId'])

# Restore latest snapshot
snaps = client.snapshots.list(rid)
if snaps:
    client.snapshots.restore(rid, {"target": "/restore", "snapshotId": snaps[0]['id']})
```

## Requirements

- Python 3.7+
- `requests >= 2.25.0`

## Next Steps

- Full examples → `examples/` directory
- Complete method docs → `API_REFERENCE.md`
- Step-by-step walkthrough → `TUTORIAL.md`
- Release checklist → `CHECKLIST.md`

---

**Version:** 1.2.1 | **License:** MIT
