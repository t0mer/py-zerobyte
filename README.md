# Zerobyte SDK

[![PyPI version](https://img.shields.io/pypi/v/py-zerobyte.svg)](https://pypi.org/project/py-zerobyte/)
[![Python versions](https://img.shields.io/pypi/pyversions/py-zerobyte.svg)](https://pypi.org/project/py-zerobyte/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/t0mer/py-zerobyte/blob/main/LICENSE)

A Python SDK for the [Zerobyte](https://github.com/nicotsx/zerobyte) backup API. Manage volumes, repositories, snapshots, backup schedules, and notifications from Python.

Zerobyte is a self-hosted backup automation server built on top of [restic](https://restic.net/). `py-zerobyte` wraps its REST API in a small, typed client, so you can script backup setup, trigger runs, browse snapshots and restore data without clicking through the web UI.

> **Unofficial project.** `py-zerobyte` is a community SDK. It is not affiliated with, endorsed by, or maintained by the Zerobyte project or its authors.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Resource IDs](#resource-ids)
- [Usage Examples](#usage-examples)
- [API Coverage](#api-coverage)
- [Server Compatibility](#server-compatibility)
- [Error Handling](#error-handling)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [More Documentation](#more-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Links](#links)
- [Changelog](#changelog)

## Features

- **Authentication**: login, logout, session info and password change via Zerobyte's `better-auth` endpoints
- **Volumes**: create, update, delete, test connection, mount/unmount, health check, list files, browse the server filesystem
- **Repositories**: manage restic repositories (local, SFTP, S3, R2, Azure, GCS, REST, rclone), run `doctor`, list rclone remotes
- **Snapshots**: list, inspect, browse files, restore, delete
- **Backup Schedules**: cron-driven schedules with retention, mirrors, per-schedule notifications, run/stop/forget
- **Notification Destinations**: Telegram, email, Pushover, ntfy, Gotify, Discord, Slack and custom Shoutrrr URLs
- **System**: server capabilities, restic password download
- **Typed exceptions** for authentication, validation, not-found and other API errors
- **One runtime dependency**: [`requests`](https://pypi.org/project/requests/)

## Requirements

- Python 3.7 or newer (`requires-python = ">=3.7"`)
- `requests >= 2.25.0` (installed automatically)
- A running Zerobyte server you can reach over HTTP(S), and a username/password account on it

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

The package is imported as `py_zerobyte`.

## Quick Start

```python
from py_zerobyte import ZerobyteClient

client = ZerobyteClient(
    url="http://localhost:4096",
    username="admin",
    password="your-password"
)

# Auto-login runs on init, so you're ready to go
session = client.auth.get_me()
print(f"Logged in as: {session['user']['username']}")

volumes = client.volumes.list()
for v in volumes:
    print(f"Volume: {v['name']}  shortId: {v['shortId']}")
```

## How It Works

- `ZerobyteClient` holds a single [`requests.Session`](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) (`client.session`).
- On creation it logs in with `POST /api/auth/sign-in/username` (unless `auto_login=False`). The server sets a session cookie, which the `requests.Session` stores and sends with every later request. The SDK does not use API keys or bearer tokens.
- Each resource group is an attribute on the client: `client.auth`, `client.volumes`, `client.repositories`, `client.snapshots`, `client.backup_schedules`, `client.notifications` and `client.system`.
- Every method sends one HTTP request and returns the parsed JSON body (a `dict` or `list`). If the body isn't JSON, you get the raw text; an empty body returns `None`.
- HTTP errors are turned into [exceptions](#error-handling).
- The SDK does not re-login when a session expires. If you get an `AuthenticationError` in a long-running script, call `client.login()` again.
- **Known issue:** `auth.logout()` and `auth.change_password()` always send the header `Origin: http://localhost:<port>` (the port comes from `url`). `better-auth` checks this header against its trusted origins, so a remote server may reject these two calls.

## Configuration

```python
client = ZerobyteClient(
    url="http://localhost:4096",   # Zerobyte server URL
    username="admin",              # Login username
    password="your-password",      # Login password
    auto_login=True                # Default: True, logs in during __init__
)

# Manual login (when auto_login=False)
client = ZerobyteClient(url=..., username=..., password=..., auto_login=False)
client.login()
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `url` | `str` | required | Base URL of the Zerobyte server, e.g. `http://localhost:4096`. A trailing `/` is stripped. |
| `username` | `str` | required | Account username. |
| `password` | `str` | required | Account password. Kept on the client (`client.password`) so `client.login()` can be called again. |
| `auto_login` | `bool` | `True` | Log in during `__init__`. Set it to `False` to log in later with `client.login()`. |

The SDK reads no environment variables or config files. Pass everything to the constructor.

### Timeouts, retries and TLS

The SDK sets **no request timeout** and **no retries**: a request waits as long as `requests` does (no timeout by default), and a failed request is raised straight away. You can tune the underlying session yourself:

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

client = ZerobyteClient(url="https://zerobyte.example.com",
                        username="admin", password="secret", auto_login=False)

# Trust a private CA (keep certificate verification on)
client.session.verify = "/path/to/ca-bundle.crt"

# Retry idempotent requests on connection errors / 502-504
retry = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504],
              allowed_methods=["GET"])   # allowed_methods needs urllib3 >= 1.26
client.session.mount("https://", HTTPAdapter(max_retries=retry))

client.login()
```

`requests` has no session-wide timeout setting, and the public SDK methods don't take a `timeout` argument.

## Resource IDs

Zerobyte identifies most resources by a **shortId** string (e.g. `"0-b-U31s"`, `"Eilm20ua"`), not by a sequential integer. Always use the `shortId` field from list/create responses when calling get/update/delete methods on volumes and repositories. Note that `repositories.create()` nests the new repository in the response, so its ID is `repo["repository"]["shortId"]`.

```python
volumes = client.volumes.list()
vol_id = volumes[0]['shortId']   # e.g. "0-b-U31s"
detail  = client.volumes.get(vol_id)
```

Exceptions:

- **Notification destinations** use their numeric `id`.
- **Snapshots** use restic's snapshot ID (the `short_id` field from `snapshots.list()`).
- **Backup schedules**: current Zerobyte servers use the schedule `shortId` in paths. Swagger-era servers (matching the bundled `swagger.json`) use the numeric `id` instead and return no `shortId` in create responses.

---

## Usage Examples

The request bodies below follow the Zerobyte API schema in [`swagger.json`](https://github.com/t0mer/py-zerobyte/blob/main/swagger.json), except where current upstream Zerobyte differs; there the examples follow current upstream and the difference is noted. Payload dicts are sent to the server as-is, so check them against your server version (see [Server Compatibility](#server-compatibility)).

### Authentication

```python
# Check whether any users exist (first-time setup)
status = client.auth.get_status()
if not status['hasUsers']:
    client.auth.register("admin", "initial-password")  # username >= 3 chars, password >= 8 chars

# Get current session / user info
session = client.auth.get_me()
print(session['user']['username'])

# Change password
client.auth.change_password("old-password", "new-password")

# Logout
client.auth.logout()
```

`client.login()` and `client.logout()` are shortcuts for `client.auth.login(username, password)` and `client.auth.logout()`.

### Volumes

```python
# List all volumes
volumes = client.volumes.list()

# Test a configuration before saving it
result = client.volumes.test_connection({
    "config": {"backend": "directory", "path": "/mnt/backup"}
})
print(result['success'], result['message'])

# Create a volume (directory backend)
volume = client.volumes.create({
    "name": "my-backup",
    "config": {
        "backend": "directory",
        "path": "/mnt/backup"
    }
})
vid = volume['shortId']

# Get, update, delete
detail  = client.volumes.get(vid)          # {"volume": {...}, "statfs": {...}}
updated = client.volumes.update(vid, {"autoRemount": True})  # create() accepts only name and config
client.volumes.delete(vid)

# Mount / unmount / health check
client.volumes.mount(vid)
client.volumes.unmount(vid)
health = client.volumes.health_check(vid)

# Browse files
files   = client.volumes.list_files(vid, path="/data")   # path is relative to the volume root
listing = client.volumes.browse_filesystem(path="/mnt")  # absolute path on the server, defaults to /
```

Volume backends in the API schema: `directory`, `nfs`, `smb`, `webdav` and `rclone`.

### Repositories

```python
# List all repositories
repos = client.repositories.list()

# Create a local repository
repo = client.repositories.create({
    "name": "local-repo",
    "compressionMode": "auto",       # "auto", "max" or "off"
    "config": {
        "backend": "local",
        "path": "/backups/repo1"
    }
})
rid = repo['repository']['shortId']   # the create response nests the repository

# Get, update (PATCH), delete
detail  = client.repositories.get(rid)
updated = client.repositories.update(rid, {"compressionMode": "max"})
client.repositories.delete(rid)

# Doctor (check + repair)
result = client.repositories.doctor(rid)

# List available rclone remotes
remotes = client.repositories.list_rclone_remotes()
```

Repository backends: `local`, `sftp`, `s3`, `r2`, `azure`, `gcs`, `rest` and `rclone`. The `local` backend fields differ between server versions: the bundled `swagger.json` requires a `name` in `config`, while current Zerobyte requires `path` (as in the example above).

### Snapshots

```python
# List snapshots for a repository (use repository shortId)
snapshots = client.snapshots.list(repository_name=rid)

# Optionally filter by backup schedule
# snapshots = client.snapshots.list(rid, backup_id="schedule-id")

if snapshots:
    snap_id = snapshots[0]['short_id']

    # Get snapshot detail
    detail = client.snapshots.get_details(rid, snap_id)

    # Browse files inside a snapshot
    files = client.snapshots.list_files(rid, snap_id, path="/home")

    # Restore (snapshotId is required; targetPath is optional)
    client.snapshots.restore(rid, {
        "snapshotId": snap_id,
        "targetPath": "/restore/path",
        "include": ["/home/user"],
        "exclude": ["/home/user/.cache"],
        "overwrite": "if-newer"      # "always", "if-changed", "if-newer" or "never"
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
    "name": "Daily Backup",          # 1-32 characters
    "repositoryId": rid,             # repository shortId
    "volumeId": volume['id'],        # the volume's numeric id
    "cronExpression": "0 2 * * *",
    "enabled": True,
    "excludePatterns": ["**/.cache/**"],
    "retentionPolicy": {
        "keepLast": 7,
        "keepDaily": 7,
        "keepWeekly": 4,
        "keepMonthly": 12
    },
    "tags": ["daily", "production"]
})
sched_id = schedule['shortId']       # see "Resource IDs" above

# Get, update (PATCH), delete
detail  = client.backup_schedules.get(sched_id)
updated = client.backup_schedules.update(sched_id, {
    "repositoryId": rid,             # repositoryId and cronExpression are required on update
    "cronExpression": "0 3 * * *",
    "enabled": False
})
client.backup_schedules.delete(sched_id)

# The schedule for one volume (a single schedule, or None if the volume has none).
# Current servers take the volume shortId; swagger-era servers take the numeric volume id.
vol_schedule = client.backup_schedules.get_for_volume(volume_id=vid)

# Trigger / stop / forget (apply the retention policy)
client.backup_schedules.run_now(sched_id)
client.backup_schedules.stop_backup(sched_id)
client.backup_schedules.run_forget(sched_id)

# Notifications per schedule
current = client.backup_schedules.get_notifications(sched_id)
client.backup_schedules.update_notifications(sched_id, {
    "assignments": [
        {
            "destinationId": 1,
            "notifyOnStart": False,
            "notifyOnSuccess": True,
            "notifyOnWarning": True,
            "notifyOnFailure": True
        }
    ]
})

# Mirrors (copy each backup to other repositories)
mirrors = client.backup_schedules.get_mirrors(sched_id)
client.backup_schedules.update_mirrors(sched_id, {
    "mirrors": [
        {"repositoryId": rid2, "enabled": True}
    ]
})
compat = client.backup_schedules.get_mirror_compatibility(sched_id)

# Reorder
client.backup_schedules.reorder({"scheduleShortIds": ["id-c", "id-a", "id-b"]})
# Swagger-era servers expect numeric ids instead: {"scheduleIds": [3, 1, 2]}
```

Retention keys: `keepLast`, `keepHourly`, `keepDaily`, `keepWeekly`, `keepMonthly`, `keepYearly` and `keepWithinDuration`.

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
        "useTLS": True,
        "username": "backup@example.com",   # optional
        "password": "app-password"          # optional
    }
})

# Get, update (PATCH), delete
detail  = client.notifications.get_destination(did)
updated = client.notifications.update_destination(did, {"name": "Renamed", "enabled": True})
client.notifications.delete_destination(did)

# Send a test message
client.notifications.test_destination(did)
```

Destination types and their required `config` fields (from `swagger.json`):

| `type` | Required fields |
|--------|-----------------|
| `telegram` | `botToken`, `chatId` |
| `email` | `from`, `to` (list), `smtpHost`, `smtpPort`, `useTLS` |
| `pushover` | `apiToken`, `userKey`, `priority` (`-1`, `0` or `1`) |
| `ntfy` | `topic`, `priority` |
| `gotify` | `serverUrl`, `token`, `priority` |
| `discord` | `webhookUrl` |
| `slack` | `webhookUrl` |
| `custom` | `shoutrrrUrl` |

### System

```python
# Server capabilities
info = client.system.get_info()
print(info['capabilities'])   # {"rclone": bool, "sysAdmin": bool}

# Download the restic repository password (requires your account password)
restic_password = client.system.download_restic_password("your-account-password")
```

The server returns the restic password as plain text, so `download_restic_password()` returns a `str`, not a `dict`. Store it somewhere safe: you need it to open your repositories with plain `restic`.

---

## API Coverage

Every method maps to one HTTP request. Path parameters are shown as `{...}`.

| Method | HTTP | Endpoint |
|--------|------|----------|
| `auth.register(username, password)` | POST | `/api/v1/auth/register` |
| `auth.login(username, password)` | POST | `/api/auth/sign-in/username` |
| `auth.logout()` | POST | `/api/auth/sign-out` |
| `auth.get_me()` | GET | `/api/auth/get-session` |
| `auth.get_status()` | GET | `/api/v1/auth/status` |
| `auth.change_password(current_password, new_password)` | POST | `/api/auth/change-password` |
| `volumes.list()` | GET | `/api/v1/volumes` |
| `volumes.create(volume_data)` | POST | `/api/v1/volumes` |
| `volumes.test_connection(volume_data)` | POST | `/api/v1/volumes/test-connection` |
| `volumes.get(volume_name)` | GET | `/api/v1/volumes/{volume_name}` |
| `volumes.update(volume_name, volume_data)` | PUT | `/api/v1/volumes/{volume_name}` |
| `volumes.delete(volume_name)` | DELETE | `/api/v1/volumes/{volume_name}` |
| `volumes.mount(volume_name)` | POST | `/api/v1/volumes/{volume_name}/mount` |
| `volumes.unmount(volume_name)` | POST | `/api/v1/volumes/{volume_name}/unmount` |
| `volumes.health_check(volume_name)` | POST | `/api/v1/volumes/{volume_name}/health-check` |
| `volumes.list_files(volume_name, path=None)` | GET | `/api/v1/volumes/{volume_name}/files?path=` |
| `volumes.browse_filesystem(path=None)` | GET | `/api/v1/volumes/filesystem/browse?path=` |
| `repositories.list()` | GET | `/api/v1/repositories` |
| `repositories.create(repository_data)` | POST | `/api/v1/repositories` |
| `repositories.get(name)` | GET | `/api/v1/repositories/{name}` |
| `repositories.update(name, repository_data)` | PATCH | `/api/v1/repositories/{name}` |
| `repositories.delete(name)` | DELETE | `/api/v1/repositories/{name}` |
| `repositories.doctor(name)` | POST | `/api/v1/repositories/{name}/doctor` |
| `repositories.list_rclone_remotes()` | GET | `/api/v1/repositories/rclone-remotes` |
| `snapshots.list(repository_name, backup_id=None)` | GET | `/api/v1/repositories/{repository_name}/snapshots?backupId=` |
| `snapshots.get_details(repository_name, snapshot_id)` | GET | `/api/v1/repositories/{repository_name}/snapshots/{snapshot_id}` |
| `snapshots.delete(repository_name, snapshot_id)` | DELETE | `/api/v1/repositories/{repository_name}/snapshots/{snapshot_id}` |
| `snapshots.list_files(repository_name, snapshot_id, path=None)` | GET | `/api/v1/repositories/{repository_name}/snapshots/{snapshot_id}/files?path=` |
| `snapshots.restore(repository_name, restore_data)` | POST | `/api/v1/repositories/{repository_name}/restore` |
| `backup_schedules.list()` | GET | `/api/v1/backups` |
| `backup_schedules.create(schedule_data)` | POST | `/api/v1/backups` |
| `backup_schedules.get(schedule_id)` | GET | `/api/v1/backups/{schedule_id}` |
| `backup_schedules.update(schedule_id, schedule_data)` | PATCH | `/api/v1/backups/{schedule_id}` |
| `backup_schedules.delete(schedule_id)` | DELETE | `/api/v1/backups/{schedule_id}` |
| `backup_schedules.get_for_volume(volume_id)` | GET | `/api/v1/backups/volume/{volume_id}` |
| `backup_schedules.run_now(schedule_id)` | POST | `/api/v1/backups/{schedule_id}/run` |
| `backup_schedules.stop_backup(schedule_id)` | POST | `/api/v1/backups/{schedule_id}/stop` |
| `backup_schedules.run_forget(schedule_id)` | POST | `/api/v1/backups/{schedule_id}/forget` |
| `backup_schedules.get_notifications(schedule_id)` | GET | `/api/v1/backups/{schedule_id}/notifications` |
| `backup_schedules.update_notifications(schedule_id, notifications_data)` | PUT | `/api/v1/backups/{schedule_id}/notifications` |
| `backup_schedules.get_mirrors(schedule_id)` | GET | `/api/v1/backups/{schedule_id}/mirrors` |
| `backup_schedules.update_mirrors(schedule_id, mirrors_data)` | PUT | `/api/v1/backups/{schedule_id}/mirrors` |
| `backup_schedules.get_mirror_compatibility(schedule_id)` | GET | `/api/v1/backups/{schedule_id}/mirrors/compatibility` |
| `backup_schedules.reorder(order_data)` | POST | `/api/v1/backups/reorder` |
| `notifications.list_destinations()` | GET | `/api/v1/notifications/destinations` |
| `notifications.create_destination(destination_data)` | POST | `/api/v1/notifications/destinations` |
| `notifications.get_destination(destination_id)` | GET | `/api/v1/notifications/destinations/{destination_id}` |
| `notifications.update_destination(destination_id, destination_data)` | PATCH | `/api/v1/notifications/destinations/{destination_id}` |
| `notifications.delete_destination(destination_id)` | DELETE | `/api/v1/notifications/destinations/{destination_id}` |
| `notifications.test_destination(destination_id)` | POST | `/api/v1/notifications/destinations/{destination_id}/test` |
| `system.get_info()` | GET | `/api/v1/system/info` |
| `system.download_restic_password(password)` | POST | `/api/v1/system/restic-password` |

All 52 operations in the bundled `swagger.json` have a matching method. Four of them (login, logout, get-session and change-password) call the newer `better-auth` routes under `/api/auth/...` instead of the `/api/v1/auth/...` routes listed in that file.

## Server Compatibility

The SDK was written against the Zerobyte API described in the bundled [`swagger.json`](https://github.com/t0mer/py-zerobyte/blob/main/swagger.json) (API version `1.0.0`, December 2025), with authentication later moved to Zerobyte's `better-auth` endpoints. Zerobyte is under active development, and newer server releases have changed parts of the API. For example:

- `POST /api/v1/auth/register` and `POST /api/v1/backups/{id}/stop` are no longer in the current upstream API client.
- `backups/reorder` takes `scheduleShortIds` (strings) instead of `scheduleIds` (numbers).
- Newer endpoints (API keys, tasks, repository stats, snapshot tags, config import/export) have no SDK method yet.

No specific Zerobyte server version is tested or pinned.

If a call fails with a `NotFoundError` or `ValidationError`, compare the payload with your server's API docs.

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
except AuthenticationError as e:       # not a subclass of APIError
    print(f"Session expired or not logged in: {e}")
except APIError as e:
    print(f"API error (HTTP {e.status_code}): {e}")
except ZerobyteError as e:
    print(f"SDK error: {e}")
```

| Exception | Raised when | Attributes |
|-----------|-------------|------------|
| `ZerobyteError` | Base class. Also raised directly for network failures (connection refused, DNS, TLS errors) | message only |
| `AuthenticationError(ZerobyteError)` | HTTP 401 | message only |
| `APIError(ZerobyteError)` | Any other HTTP status >= 400 (e.g. 403, 409, 500) | `status_code`, `response` |
| `ValidationError(APIError)` | HTTP 400 | `status_code`, `response` |
| `NotFoundError(APIError)` | HTTP 404 | `status_code`, `response` |

For `APIError` and `ValidationError`, the message is the server's `message` field when the response body has one. `e.response` is the underlying `requests.Response`.

## Security Notes

- **Use HTTPS** for any server that isn't on `localhost`. Credentials and the session cookie travel with every request.
- **Keep TLS verification on.** For self-signed certificates, point `client.session.verify` at your CA bundle instead of disabling verification.
- **Don't hard-code credentials.** Load them from environment variables or a secrets manager in your own code. The client keeps the password in memory (`client.password`) so it can log in again.
- **Protect the restic password.** Anyone with it and access to the repository storage can read your backups.
- **Notification configs contain secrets** (bot tokens, SMTP passwords, webhook URLs). Treat scripts that create them like any other secret-bearing file.
- Use a dedicated Zerobyte account for automation where possible, and call `client.logout()` when a script is done (see the known issue with `logout()` under [How It Works](#how-it-works)).

## Troubleshooting

- **`AuthenticationError` right after creating the client**: the login was rejected (HTTP 401). Check the URL, username and password. Pass `auto_login=False` to create the client without logging in.
- **`AuthenticationError` in a long-running script**: the session expired. Call `client.login()` and retry.
- **`NotFoundError` on get/update/delete**: you probably passed a numeric `id` where a `shortId` is expected (see [Resource IDs](#resource-ids)), or your server version uses a different endpoint (see [Server Compatibility](#server-compatibility)).
- **`ValidationError`**: the request body doesn't match the server schema. `e.response.json()` usually shows which field is wrong.
- **`ZerobyteError: Request failed: ...`**: a network or TLS problem. Check that the server is reachable and that the certificate is trusted.
- **A call hangs**: the SDK sets no timeout. See [Timeouts, retries and TLS](#timeouts-retries-and-tls).

---

## Development

```bash
# Install with dev extras (pytest, pytest-cov, black, flake8)
pip install -e ".[dev]"

# Run tests
pytest

# Format
black py_zerobyte/

# Lint
flake8 py_zerobyte/
```

The tests in `tests/test_client.py` mock `requests.Session`, so they don't need a Zerobyte server.

Project layout:

```
py_zerobyte/
├── __init__.py          # ZerobyteClient + exceptions, __version__
├── client.py            # ZerobyteClient, session handling, error mapping
├── exceptions.py        # Exception hierarchy
├── auth.py              # client.auth
├── volumes.py           # client.volumes
├── repositories.py      # client.repositories
├── snapshots.py         # client.snapshots
├── backup_schedules.py  # client.backup_schedules
├── notifications.py     # client.notifications
└── system.py            # client.system
examples/                # runnable example scripts
tests/                   # pytest suite
quickstart.py            # example script with editable constants
swagger.json             # Zerobyte OpenAPI spec the SDK was built against
```

Releases are published to PyPI by the `Publish pypi package` GitHub Actions workflow (`.github/workflows/python-publish.yml`), which runs when a GitHub release is published or on manual dispatch. The version is set in `pyproject.toml`, `setup.py` and `py_zerobyte/__init__.py`, and all three must match.

## More Documentation

The repository has more guides and scripts. Some of them predate the latest API changes. Where they disagree with this README, trust this README.

- [API Reference](https://github.com/t0mer/py-zerobyte/blob/main/API_REFERENCE.md)
- [Quick Start guide](https://github.com/t0mer/py-zerobyte/blob/main/QUICKSTART.md)
- [Tutorial](https://github.com/t0mer/py-zerobyte/blob/main/TUTORIAL.md)
- [Installation guide](https://github.com/t0mer/py-zerobyte/blob/main/INSTALL.md)
- [Example scripts](https://github.com/t0mer/py-zerobyte/tree/main/examples)
- [`quickstart.py`](https://github.com/t0mer/py-zerobyte/blob/main/quickstart.py): an example script with editable constants

## Contributing

Issues and pull requests are welcome at [github.com/t0mer/py-zerobyte](https://github.com/t0mer/py-zerobyte). Please run `pytest`, `black` and `flake8` before opening a PR, and describe which Zerobyte server version you tested against.

## License

MIT. See [LICENSE](https://github.com/t0mer/py-zerobyte/blob/main/LICENSE).

## Links

- PyPI: https://pypi.org/project/py-zerobyte/
- Issues: https://github.com/t0mer/py-zerobyte/issues
- Zerobyte (upstream server): https://github.com/nicotsx/zerobyte

## Changelog

### 1.3.0
- Migrated auth to `better-auth` endpoints
- Volumes now use `shortId` (string) as identifier in all path parameters
- Repositories `update()` uses PATCH; added `list_rclone_remotes()`
- Backup schedules restructured to flat `/api/v1/backups` API
- Notifications path updated; `update_destination()` uses PATCH
- `system.download_restic_password()` now requires account password
- **Breaking:** `repositories.list()` no longer takes a `volume_id` parameter

### 1.2.1
- Fixes to API calls and examples

### 1.2.0
- Installation and naming fixes

### 1.1.0
- Not published to PyPI

### 1.0.0
- Initial release (not published to PyPI)
