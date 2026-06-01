# API Reference — Zerobyte SDK

Complete reference for every public method in `py-zerobyte`.

## Table of Contents

- [ZerobyteClient](#zerobyteclient)
- [AuthAPI](#authapi)
- [VolumesAPI](#volumesapi)
- [RepositoriesAPI](#repositoriesapi)
- [SnapshotsAPI](#snapshotsapi)
- [BackupSchedulesAPI](#backupschedulesapi)
- [NotificationsAPI](#notificationsapi)
- [SystemAPI](#systemapi)
- [Exceptions](#exceptions)

---

## ZerobyteClient

```python
from py_zerobyte import ZerobyteClient

client = ZerobyteClient(url, username, password, auto_login=True)
```

**Parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | str | — | Base URL of the Zerobyte server (e.g. `http://localhost:4096`) |
| `username` | str | — | Login username |
| `password` | str | — | Login password |
| `auto_login` | bool | `True` | Call `login()` automatically during `__init__` |

**Attributes** — API module instances

| Attribute | Type |
|---|---|
| `client.auth` | `AuthAPI` |
| `client.volumes` | `VolumesAPI` |
| `client.repositories` | `RepositoriesAPI` |
| `client.snapshots` | `SnapshotsAPI` |
| `client.backup_schedules` | `BackupSchedulesAPI` |
| `client.notifications` | `NotificationsAPI` |
| `client.system` | `SystemAPI` |

**Methods**

`client.login()` — Log in using the stored username/password. Called automatically when `auto_login=True`.

`client.logout()` — Log out the current session.

---

## AuthAPI

Access via `client.auth`.

### `register(username, password)`

Register a new user account.

| Parameter | Type | Description |
|---|---|---|
| `username` | str | Minimum 3 characters |
| `password` | str | Minimum 8 characters |

Returns `dict` with `message`, `success`, `user`.

---

### `login(username, password)`

Authenticate and start a session. Sets the `zerobyte.session_token` cookie on the underlying `requests.Session`.

Returns `dict` with `user` info and `token`.

---

### `logout()`

End the current session.

Returns `dict` with `success: true`.

---

### `get_me()`

Return the current session and authenticated user.

```python
session = client.auth.get_me()
# {"session": {...}, "user": {"username": "admin", "role": "admin", ...}}
```

Returns `dict` with `session` and `user` keys.

---

### `get_status()`

Check whether any users are registered (useful for first-run setup).

```python
status = client.auth.get_status()
# {"hasUsers": true}
```

Returns `dict` with `hasUsers` bool.

---

### `change_password(current_password, new_password)`

Change the authenticated user's password.

| Parameter | Type | Description |
|---|---|---|
| `current_password` | str | Current password |
| `new_password` | str | New password (min 8 chars) |

Returns `dict`.

---

## VolumesAPI

Access via `client.volumes`.

> **Note:** All per-volume methods accept the volume's **`shortId`** string (e.g. `"0-b-U31s"`), not the numeric `id`.

### `list()`

List all configured volumes.

Returns `list[dict]` — each item contains `id`, `shortId`, `name`, `type`, `status`, `config`, etc.

---

### `create(volume_data)`

Create a new volume.

| Key | Type | Required | Description |
|---|---|---|---|
| `name` | str | yes | Display name |
| `autoRemount` | bool | no | Remount automatically on server restart |
| `config` | dict | yes | Backend config — must include `"backend"` key |

Common `config` backends:

```python
# Local directory
{"backend": "directory", "path": "/mnt/backup"}

# NFS / CIFS / block device — use appropriate backend key
```

Returns `dict` with the created volume.

---

### `test_connection(volume_data)`

Validate volume config without persisting it.

Returns `dict` with test result.

---

### `get(volume_name)`

Get a volume by shortId.

Returns `dict` — wraps the volume under a `"volume"` key.

---

### `update(volume_name, volume_data)`

Update a volume's configuration.

Returns `dict` with the updated volume.

---

### `delete(volume_name)`

Delete a volume.

Returns `dict`.

---

### `mount(volume_name)`

Mount a volume.

Returns `dict`.

---

### `unmount(volume_name)`

Unmount a volume.

Returns `dict`.

---

### `health_check(volume_name)`

Run a health check on a volume.

Returns `dict`.

---

### `list_files(volume_name, path=None)`

List files at `path` within a volume.

| Parameter | Type | Description |
|---|---|---|
| `volume_name` | str | Volume shortId |
| `path` | str \| None | Subdirectory relative to volume root (default: root) |

Returns `dict` with `files` list.

---

### `browse_filesystem(path=None)`

Browse the server's filesystem (not limited to a volume).

| Parameter | Type | Description |
|---|---|---|
| `path` | str \| None | Absolute server path (default: `/`) |

Returns `dict` with `directories` and `files`.

---

## RepositoriesAPI

Access via `client.repositories`.

> **Note:** Get/update/delete methods accept the repository's **`shortId`** string.

### `list()`

List all repositories.

Returns `list[dict]` — each item contains `id`, `shortId`, `name`, `type`, `config`, `status`, etc.

---

### `create(repository_data)`

Create a new repository.

| Key | Type | Required | Description |
|---|---|---|---|
| `name` | str | yes | Display name |
| `config` | dict | yes | Backend config with `"backend"` key |
| `compressionMode` | str | no | `"auto"` (default), `"max"`, or `"off"` |

Common `config.backend` values: `"local"`, `"sftp"`, `"s3"`, `"r2"`, `"azure"`, `"gcs"`, `"rest"`, `"rclone"`.

Returns `dict` with the created repository.

---

### `get(name)`

Get a repository by shortId.

Returns `dict`.

---

### `update(name, repository_data)`

Update a repository (HTTP PATCH — send only the fields to change).

| Key | Type | Description |
|---|---|---|
| `name` | str | New display name |
| `compressionMode` | str | `"auto"`, `"max"`, or `"off"` |

Returns `dict`.

---

### `delete(name)`

Delete a repository.

Returns `dict`.

---

### `doctor(name)`

Run the restic `doctor` command to check and repair repository integrity.

Returns `dict` with doctor output.

---

### `list_rclone_remotes()`

List rclone remotes configured on the server.

Returns `list[str]`.

---

## SnapshotsAPI

Access via `client.snapshots`.

### `list(repository_name, backup_id=None)`

List snapshots in a repository.

| Parameter | Type | Description |
|---|---|---|
| `repository_name` | str | Repository shortId |
| `backup_id` | str \| None | Filter by backup schedule ID |

Returns `list[dict]` — each item contains `id`, `time`, `tags`, `paths`, `hostname`, etc.

---

### `get_details(repository_name, snapshot_id)`

Get full metadata for a single snapshot.

Returns `dict`.

---

### `delete(repository_name, snapshot_id)`

Delete a snapshot from the repository.

Returns `dict`.

---

### `list_files(repository_name, snapshot_id, path=None)`

Browse the file tree inside a snapshot.

| Parameter | Type | Description |
|---|---|---|
| `path` | str \| None | Path within the snapshot to list |

Returns `dict` with `files`.

---

### `restore(repository_name, restore_data)`

Restore files from a repository snapshot.

| Key | Type | Required | Description |
|---|---|---|---|
| `target` | str | yes | Destination path on the server |
| `snapshotId` | str | no | Specific snapshot (omit to use latest) |
| `include` | list[str] | no | Paths to include |
| `exclude` | list[str] | no | Paths to exclude |

Returns `dict`.

---

## BackupSchedulesAPI

Access via `client.backup_schedules`.

> **Note:** All per-schedule methods accept the schedule's **`shortId`** string. `repositoryId` is the repository's **`shortId`**; `volumeId` is the volume's numeric `id`.

### `list()`

List all backup schedules.

Returns `list[dict]`.

---

### `create(schedule_data)`

Create a backup schedule.

| Key | Type | Required | Description |
|---|---|---|---|
| `name` | str | yes | Display name (1–32 chars) |
| `repositoryId` | str | yes | Target repository shortId |
| `volumeId` | int | yes | Source volume numeric id |
| `cronExpression` | str | yes | Cron expression (e.g. `"0 2 * * *"`) |
| `enabled` | bool | yes | Whether to run on schedule |
| `backupPaths` | list[str] | no | Paths to include in backup |
| `excludePatterns` | list[str] | no | Glob patterns to exclude |
| `excludeIfPresent` | list[str] | no | Skip dirs containing these filenames |
| `retentionPolicy` | dict | no | Retention rules (see below) |
| `tags` | list[str] | no | Tags applied to snapshots |

Retention policy keys: `keepLast`, `keepHourly`, `keepDaily`, `keepWeekly`, `keepMonthly`, `keepYearly`, `keepWithinDuration`.

Returns `dict` with the created schedule including its `shortId`.

---

### `get(schedule_id)`

Get a schedule by shortId.

Returns `dict`.

---

### `update(schedule_id, schedule_data)`

Update a schedule (HTTP PATCH). `cronExpression` and `repositoryId` are required in the body.

Returns `dict`.

---

### `delete(schedule_id)`

Delete a schedule.

Returns `dict`.

---

### `get_for_volume(volume_id)`

List all schedules associated with a specific volume (numeric id).

Returns `list[dict]`.

---

### `run_now(schedule_id)`

Trigger a backup immediately, outside the cron schedule.

Returns `dict`.

---

### `stop_backup(schedule_id)`

Abort a running backup.

Returns `dict`.

---

### `run_forget(schedule_id)`

Apply the retention policy (run `restic forget`) without running a backup.

Returns `dict`.

---

### `get_notifications(schedule_id)`

Retrieve notification settings for this schedule.

Returns `dict`.

---

### `update_notifications(schedule_id, notifications_data)`

Configure which notification destinations receive results for this schedule.

| Key | Type | Description |
|---|---|---|
| `onSuccess` | bool | Notify on successful backup |
| `onFailure` | bool | Notify on failure |
| `destinations` | list[int] | Notification destination IDs |

Returns `dict`.

---

### `get_mirrors(schedule_id)`

Get mirror repository configuration.

Returns `dict`.

---

### `update_mirrors(schedule_id, mirrors_data)`

Configure mirror repositories.

| Key | Type | Description |
|---|---|---|
| `enabled` | bool | Enable mirroring |
| `repositories` | list[str] | Target repository shortIds |

Returns `dict`.

---

### `get_mirror_compatibility(schedule_id)`

Check whether configured mirrors are compatible with this schedule.

Returns `dict`.

---

### `reorder(order_data)`

Change the execution order of schedules.

| Key | Type | Description |
|---|---|---|
| `scheduleIds` | list[str] | Schedule shortIds in desired order |

Returns `dict`.

---

## NotificationsAPI

Access via `client.notifications`.

### `list_destinations()`

List all configured notification destinations.

Returns `list[dict]` — each item contains `id`, `name`, `type`, `enabled`, `status`, etc.

---

### `create_destination(destination_data)`

Create a notification destination.

| Key | Type | Required | Description |
|---|---|---|---|
| `name` | str | yes | Display name |
| `config` | dict | yes | Provider config — must include `"type"` key |

Supported `config.type` values and required fields:

| Type | Required config fields |
|---|---|
| `telegram` | `botToken`, `chatId` |
| `email` | `from`, `to` (list), `smtpHost`, `smtpPort` |
| `pushover` | `apiToken`, `userKey`, `priority` |
| `ntfy` | `topic`, `serverUrl` |
| `discord` | `webhookUrl` |
| `slack` | `webhookUrl` |
| `webhook` | `url` |

Returns `dict` with the created destination.

---

### `get_destination(destination_id)`

Get a destination by numeric id.

Returns `dict`.

---

### `update_destination(destination_id, destination_data)`

Update a destination (HTTP PATCH).

Returns `dict`.

---

### `delete_destination(destination_id)`

Delete a destination.

Returns `dict`.

---

### `test_destination(destination_id)`

Send a test message to the destination.

Returns `dict`.

---

## SystemAPI

Access via `client.system`.

### `get_info()`

Return server capabilities.

```python
info = client.system.get_info()
# {"capabilities": {"rclone": false, "sysAdmin": true}}
```

Returns `dict`.

---

### `download_restic_password(password)`

Retrieve the restic repository encryption password. Requires the caller's account password for verification.

| Parameter | Type | Description |
|---|---|---|
| `password` | str | Current account password |

Returns `dict`.

---

## Exceptions

```
ZerobyteError               ← base; wraps connection / SDK errors
├── AuthenticationError     ← HTTP 401
└── APIError                ← all HTTP 4xx/5xx errors
    │   .status_code (int)
    │   .response (requests.Response)
    ├── NotFoundError       ← HTTP 404
    └── ValidationError     ← HTTP 400
```

### Usage

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
    vol = client.volumes.get("bad-id")
except NotFoundError as e:
    print(f"Not found (HTTP {e.status_code}): {e}")

try:
    client.volumes.create({})
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    client.volumes.list()
except APIError as e:
    print(f"API error (HTTP {e.status_code}): {e}")
except ZerobyteError as e:
    print(f"SDK error: {e}")
```
