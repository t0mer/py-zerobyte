# Tutorial — Zerobyte SDK

A step-by-step guide to connecting, setting up backups, and restoring data.

## Table of Contents

1. [Installation](#installation)
2. [First Connection](#first-connection)
3. [Working with Volumes](#working-with-volumes)
4. [Setting Up a Repository](#setting-up-a-repository)
5. [Creating a Backup Schedule](#creating-a-backup-schedule)
6. [Running and Monitoring Backups](#running-and-monitoring-backups)
7. [Working with Snapshots](#working-with-snapshots)
8. [Configuring Notifications](#configuring-notifications)
9. [System Information](#system-information)
10. [Best Practices](#best-practices)

---

## Installation

```bash
pip install py-zerobyte
```

Verify:

```bash
python -c "from py_zerobyte import ZerobyteClient; print('OK')"
```

---

## First Connection

```python
from py_zerobyte import ZerobyteClient, AuthenticationError

try:
    client = ZerobyteClient(
        url="http://localhost:4096",
        username="admin",
        password="your-password"
    )
except AuthenticationError:
    print("Login failed — check your credentials.")
    raise
```

The client logs in automatically on init and stores the session cookie. All subsequent calls reuse the same session.

### Verify the connection

```python
session = client.auth.get_me()
print(f"Connected as: {session['user']['username']}")
print(f"Role: {session['user']['role']}")

# Check server capabilities
info = client.system.get_info()
print(f"Capabilities: {info['capabilities']}")
```

### First-time setup

If the server has no users yet, register one first:

```python
status = client.auth.get_status()
if not status['hasUsers']:
    client = ZerobyteClient(url="http://localhost:4096",
                            username="", password="", auto_login=False)
    client.auth.register("admin", "strong-password-here")
    client.login()   # log in with the new account
```

---

## Working with Volumes

A **volume** is a storage location the Zerobyte server can access. Volumes use a `shortId` string (e.g. `"0-b-U31s"`) as their path identifier.

### List existing volumes

```python
volumes = client.volumes.list()
for v in volumes:
    print(f"{v['name']}  shortId={v['shortId']}  status={v['status']}")
```

### Create a volume

```python
volume = client.volumes.create({
    "name": "backup-storage",
    "autoRemount": True,
    "config": {
        "backend": "directory",
        "path": "/mnt/backup"
    }
})
vid = volume['shortId']
print(f"Created: {volume['name']}  shortId={vid}")
```

### Mount / unmount

```python
client.volumes.mount(vid)
print("Mounted")

client.volumes.unmount(vid)
print("Unmounted")
```

### Health check

```python
health = client.volumes.health_check(vid)
print(f"Health: {health}")
```

### Browse files

```python
# Files inside a volume
files = client.volumes.list_files(vid, path="/")
for f in files.get('files', []):
    print(f"  {f['name']}  ({f['type']})")

# Raw server filesystem (not limited to a volume)
listing = client.volumes.browse_filesystem(path="/mnt")
for d in listing.get('directories', []):
    print(f"  {d['path']}")
```

---

## Setting Up a Repository

A **repository** is a restic backup destination. It stores deduplicated, encrypted snapshots.

```python
repo = client.repositories.create({
    "name": "production-backups",
    "compressionMode": "auto",
    "config": {
        "backend": "local",
        "path": "/mnt/backup/restic-repo"
    }
})
rid = repo['shortId']
print(f"Repository: {repo['name']}  shortId={rid}")
```

### Cloud backends

```python
# Cloudflare R2
repo = client.repositories.create({
    "name": "r2-offsite",
    "compressionMode": "auto",
    "config": {
        "backend": "r2",
        "bucket": "my-zerobyte-backups",
        "accessKeyId": "...",
        "secretAccessKey": "...",
        "endpoint": "https://<account>.r2.cloudflarestorage.com"
    }
})
```

### Repository health

```python
result = client.repositories.doctor(rid)
print(f"Doctor result: {result}")
```

---

## Creating a Backup Schedule

Schedules define **what** to back up, **when**, and **how long to keep** snapshots.

```python
schedule = client.backup_schedules.create({
    "name": "Daily Server Backup",
    "repositoryId": rid,          # repository shortId
    "volumeId": 1,                # volume numeric id (from volumes.list()[n]['id'])
    "cronExpression": "0 2 * * *",  # 2 AM every day
    "enabled": True,

    # What to back up
    "backupPaths": ["/home", "/etc", "/var/www"],

    # Exclusion rules (glob patterns)
    "excludePatterns": [
        "**/.cache/**",
        "**/node_modules/**",
        "**/__pycache__/**"
    ],

    # Retention policy
    "retentionPolicy": {
        "keepLast": 7,
        "keepDaily": 7,
        "keepWeekly": 4,
        "keepMonthly": 12,
        "keepYearly": 3
    },

    "tags": ["production", "daily"]
})

sched_id = schedule['shortId']
print(f"Schedule created: {schedule['name']}  shortId={sched_id}")
```

### Update a schedule

`update()` requires `cronExpression` and `repositoryId` even when only changing other fields:

```python
client.backup_schedules.update(sched_id, {
    "repositoryId": rid,
    "cronExpression": "0 3 * * *",   # move to 3 AM
    "enabled": True
})
```

---

## Running and Monitoring Backups

### Trigger immediately

```python
client.backup_schedules.run_now(sched_id)
print("Backup started")
```

### Stop a running backup

```python
client.backup_schedules.stop_backup(sched_id)
```

### Apply retention (forget old snapshots)

```python
client.backup_schedules.run_forget(sched_id)
```

### Check schedule status

```python
schedules = client.backup_schedules.list()
for s in schedules:
    state = "enabled" if s['enabled'] else "disabled"
    print(f"{s['name']}  [{state}]  next={s.get('nextBackupAt')}")
    if s.get('lastBackupStatus'):
        print(f"  last: {s['lastBackupStatus']}  at {s.get('lastBackupAt')}")
```

### All schedules for a specific volume

```python
vol_schedules = client.backup_schedules.get_for_volume(volume_id=1)
print(f"{len(vol_schedules)} schedule(s) for volume 1")
```

---

## Working with Snapshots

### List snapshots

```python
snapshots = client.snapshots.list(rid)
print(f"{len(snapshots)} snapshot(s)")
for s in snapshots[:5]:
    print(f"  {s['id']}  {s.get('time')}  tags={s.get('tags', [])}")
```

### Inspect a snapshot

```python
if snapshots:
    snap_id = snapshots[0]['id']
    detail = client.snapshots.get_details(rid, snap_id)
    print(f"Paths: {detail.get('paths')}")
    print(f"Hostname: {detail.get('hostname')}")
```

### Browse files inside a snapshot

```python
files = client.snapshots.list_files(rid, snap_id, path="/home")
for f in files.get('files', []):
    print(f"  {f['name']}")
```

### Restore

```python
# Restore specific paths from the latest snapshot
client.snapshots.restore(rid, {
    "target": "/restore/2026-06-01",
    "include": ["/home/user/documents"],
    "exclude": ["/home/user/documents/tmp"]
})
print("Restore initiated")

# Restore from a specific snapshot
client.snapshots.restore(rid, {
    "target": "/restore/specific",
    "snapshotId": snap_id,
    "include": ["/etc"]
})
```

### Delete a snapshot

```python
client.snapshots.delete(rid, snap_id)
print("Snapshot deleted")
```

---

## Configuring Notifications

Zerobyte supports Telegram, email, Pushover, ntfy, Discord, Slack, and generic webhooks.

### Create a Telegram destination

The destination `type` goes **inside** the `config` dict:

```python
dest = client.notifications.create_destination({
    "name": "Telegram Alerts",
    "config": {
        "type": "telegram",
        "botToken": "123456789:AAFxxxx",
        "chatId": "-1001234567890"
    }
})
dest_id = dest['id']
```

### Create an email destination

```python
client.notifications.create_destination({
    "name": "Admin Email",
    "config": {
        "type": "email",
        "from": "backup@example.com",
        "to": ["admin@example.com"],
        "smtpHost": "smtp.gmail.com",
        "smtpPort": 587,
        "useTLS": True,
        "username": "backup@example.com",
        "password": "app-specific-password"
    }
})
```

### Test a destination

```python
result = client.notifications.test_destination(dest_id)
print(f"Test result: {result}")
```

### Link a destination to a backup schedule

```python
client.backup_schedules.update_notifications(sched_id, {
    "onSuccess": False,   # don't notify on success
    "onFailure": True,    # always notify on failure
    "destinations": [dest_id]
})
```

### Mirror backups to a second repository

```python
rid2 = "other-repo-shortid"
client.backup_schedules.update_mirrors(sched_id, {
    "enabled": True,
    "repositories": [rid2]
})

# Verify compatibility
compat = client.backup_schedules.get_mirror_compatibility(sched_id)
print(f"Mirror compatibility: {compat}")
```

---

## System Information

```python
info = client.system.get_info()
caps = info['capabilities']
print(f"rclone available: {caps['rclone']}")
print(f"sysAdmin: {caps['sysAdmin']}")

# Retrieve the restic encryption password (requires your account password)
result = client.system.download_restic_password("your-account-password")
```

---

## Best Practices

### Always use shortId for path parameters

```python
# Correct
vols = client.volumes.list()
vid = vols[0]['shortId']   # "0-b-U31s"
client.volumes.mount(vid)

# Wrong — numeric id is NOT the path parameter
# client.volumes.mount(vols[0]['id'])
```

### Reuse the client

```python
# Good — one session, one login
client = ZerobyteClient(url=..., username=..., password=...)
volumes = client.volumes.list()
repos   = client.repositories.list()

# Bad — logs in on every iteration
for item in data:
    c = ZerobyteClient(...)   # unnecessary round-trip
```

### Handle errors explicitly

```python
from py_zerobyte import AuthenticationError, NotFoundError, ValidationError, APIError

try:
    schedule = client.backup_schedules.get("non-existent")
except NotFoundError:
    print("Schedule not found")
except APIError as e:
    print(f"Unexpected error (HTTP {e.status_code}): {e}")
```

### Cron expression reference

```python
"0 * * * *"      # every hour, on the hour
"0 2 * * *"      # every day at 2 AM
"0 3 * * 0"      # every Sunday at 3 AM
"0 4 1 * *"      # 1st of each month at 4 AM
"0 0 1 1 *"      # 1st January every year
```

### Retention policy guidance

```python
"retentionPolicy": {
    "keepLast": 7,       # always keep the 7 most recent snapshots
    "keepDaily": 30,     # one per day for the last 30 days
    "keepWeekly": 12,    # one per week for the last 12 weeks
    "keepMonthly": 24,   # one per month for the last 24 months
    "keepYearly": 5      # one per year for the last 5 years
}
```

---

## Next Steps

- **All method signatures** → `API_REFERENCE.md`
- **Working examples** → `examples/` directory
- **Release process** → `CHECKLIST.md`
- **Issues / questions** → https://github.com/t0mer/py-zerobyte/issues
