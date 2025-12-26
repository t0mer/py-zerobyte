# Zerobyte SDK Tutorial

A step-by-step guide for getting started with the Zerobyte SDK.

## Table of Contents

1. [Installation](#installation)
2. [First Connection](#first-connection)
3. [Working with Volumes](#working-with-volumes)
4. [Setting Up Backups](#setting-up-backups)
5. [Managing Snapshots](#managing-snapshots)
6. [Configuring Notifications](#configuring-notifications)
7. [Monitoring Your System](#monitoring-your-system)
8. [Best Practices](#best-practices)

## Installation

First, install the SDK using pip:

```bash
pip install py-zerobyte
```

Verify the installation:

```bash
python -c "from py_zerobyte import ZerobyteClient; print('✓ Installed successfully')"
```

## First Connection

### Step 1: Import the SDK

```python
from py_zerobyte import ZerobyteClient
```

### Step 2: Initialize the Client

```python
client = ZerobyteClient(
    url="http://localhost:4096",  # Your Zerobyte API URL
    username="admin",              # Your username
    password="your-password"       # Your password
)
```

The client automatically logs in when initialized. If you prefer manual login:

```python
client = ZerobyteClient(
    url="http://localhost:4096",
    username="admin",
    password="your-password",
    auto_login=False  # Disable auto-login
)

# Login manually
client.login()
```

### Step 3: Verify Connection

```python
# Get current user information
user = client.auth.get_me()
print(f"Connected as: {user['user']['username']}")

# Get system information
system_info = client.system.get_info()
print(f"Zerobyte version: {system_info['version']}")
```

## Working with Volumes

### List Existing Volumes

```python
volumes = client.volumes.list()
for volume in volumes:
    print(f"- {volume['name']} (Mounted: {volume['mounted']})")
```

### Create a New Volume

```python
volume = client.volumes.create({
    "name": "my-backup-drive",
    "device": "/dev/sdb1",          # Your storage device
    "mountPoint": "/mnt/backups",   # Where to mount it
    "filesystem": "ext4",           # Filesystem type
    "autoRemount": True,            # Auto-mount on startup
    "readonly": False,              # Read-write access
    "options": []                   # Additional mount options
})

volume_id = volume['id']
print(f"Created volume: {volume['name']} (ID: {volume_id})")
```

### Mount the Volume

```python
client.volumes.mount(volume_id)
print("Volume mounted successfully")
```

### Check Volume Health

```python
health = client.volumes.health_check(volume_id)
print(f"Volume health: {health['status']}")
```

### Browse Volume Files

```python
files = client.volumes.list_files(volume_id, path="/")
for file in files:
    print(f"- {file['name']} ({file['type']})")
```

## Setting Up Backups

### Step 1: Create a Repository

A repository is where your backups are stored.

```python
repository = client.repositories.create(
    volume_id=volume_id,
    repository_data={
        "name": "production-backups",
        "type": "local",
        "config": {
            "path": "/mnt/backups/restic-repo"
        }
    }
)

repo_id = repository['id']
print(f"Created repository: {repository['name']} (ID: {repo_id})")
```

### Step 2: Create a Backup Schedule

```python
schedule = client.backup_schedules.create(
    volume_id=volume_id,
    repository_id=repo_id,
    schedule_data={
        "name": "Daily Server Backup",
        "schedule": "0 2 * * *",  # Cron: Every day at 2 AM
        "enabled": True,
        
        # What to backup
        "backupPaths": [
            "/home",
            "/etc",
            "/var/www"
        ],
        
        # What to exclude
        "excludePaths": [
            "/home/*/.cache",
            "/home/*/tmp",
            "/var/www/cache"
        ],
        
        # Retention policy
        "retention": {
            "keepLast": 7,      # Keep last 7 snapshots
            "keepDaily": 7,     # Keep daily backups for 7 days
            "keepWeekly": 4,    # Keep weekly backups for 4 weeks
            "keepMonthly": 12,  # Keep monthly backups for 12 months
            "keepYearly": 3     # Keep yearly backups for 3 years
        },
        
        # Tags for organization
        "tags": ["production", "daily", "automated"]
    }
)

schedule_id = schedule['id']
print(f"Created schedule: {schedule['name']} (ID: {schedule_id})")
```

### Step 3: Run Initial Backup

Don't wait for the schedule - run your first backup now:

```python
print("Starting initial backup...")
client.backup_schedules.run_now(volume_id, repo_id, schedule_id)
print("Backup started! This may take a while.")
```

## Managing Snapshots

### List All Snapshots

```python
snapshots = client.snapshots.list(volume_id, repo_id)
print(f"Found {len(snapshots)} snapshots:")

for snapshot in snapshots[:5]:  # Show first 5
    print(f"- {snapshot['id']}")
    print(f"  Time: {snapshot['time']}")
    print(f"  Tags: {', '.join(snapshot.get('tags', []))}")
```

### Browse Snapshot Contents

```python
snapshot_id = snapshots[0]['id']  # Most recent snapshot

files = client.snapshots.list_files(
    volume_id=volume_id,
    repository_id=repo_id,
    snapshot_id=snapshot_id,
    path="/home"
)

print("Files in snapshot /home:")
for file in files:
    print(f"- {file['name']}")
```

### Restore from Snapshot

```python
# Restore specific files to a target location
restore_response = client.snapshots.restore(
    volume_id=volume_id,
    repository_id=repo_id,
    snapshot_id=snapshot_id,
    restore_data={
        "target": "/restore/2024-12-26",  # Where to restore
        "include": ["/home/user/documents"],  # What to restore
        "exclude": ["/home/user/documents/temp"]  # What to skip
    }
)

print("Restore initiated!")
print("Files will be restored to /restore/2024-12-26")
```

## Configuring Notifications

### Create Email Notification

```python
email_notification = client.notifications.create_destination({
    "name": "Admin Email Alerts",
    "type": "email",
    "config": {
        "to": "admin@example.com",
        "from": "backup@example.com",
        "smtpHost": "smtp.gmail.com",
        "smtpPort": 587,
        "username": "backup@example.com",
        "password": "your-app-password",  # Use app-specific password
        "useTLS": True
    }
})

notification_id = email_notification['id']
print(f"Created notification: {email_notification['name']}")
```

### Test Notification

```python
test_result = client.notifications.test_destination(notification_id)
if test_result['success']:
    print("✓ Test email sent successfully!")
else:
    print(f"✗ Test failed: {test_result.get('message')}")
```

### Link Notification to Backup Schedule

```python
client.backup_schedules.update_notifications(
    volume_id=volume_id,
    repository_id=repo_id,
    schedule_id=schedule_id,
    notifications_data={
        "onSuccess": True,   # Notify on successful backup
        "onFailure": True,   # Notify on failed backup
        "destinations": [notification_id]  # Which notifications to use
    }
)

print("Notifications configured for backup schedule")
```

## Monitoring Your System

### Get Overall Status

```python
# List all volumes
volumes = client.volumes.list()
print(f"Volumes: {len(volumes)}")

# For each volume, get details
for volume in volumes:
    print(f"\n{volume['name']}:")
    
    # Check health
    try:
        health = client.volumes.health_check(volume['id'])
        print(f"  Health: {health['status']}")
    except:
        print(f"  Health: Unknown")
    
    # List repositories
    repos = client.repositories.list(volume['id'])
    print(f"  Repositories: {len(repos)}")
    
    for repo in repos:
        # Count snapshots
        snapshots = client.snapshots.list(volume['id'], repo['id'])
        print(f"    - {repo['name']}: {len(snapshots)} snapshots")
```

### Check Backup Schedule Status

```python
schedules = client.backup_schedules.list(volume_id, repo_id)

for schedule in schedules:
    status = "✓ Enabled" if schedule['enabled'] else "✗ Disabled"
    print(f"{schedule['name']}: {status}")
    print(f"  Schedule: {schedule['schedule']}")
    
    # Check last run
    if 'lastRun' in schedule:
        last_run = schedule['lastRun']
        print(f"  Last run: {last_run['time']} - {last_run['status']}")
```

## Best Practices

### 1. Error Handling

Always wrap API calls in try-except blocks:

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
    
    volume = client.volumes.get(999)  # May not exist
    
except AuthenticationError:
    print("Invalid credentials!")
except NotFoundError:
    print("Volume not found!")
except ValidationError as e:
    print(f"Validation error: {e}")
except APIError as e:
    print(f"API error: {e}")
```

### 2. Session Management

Reuse the client instance instead of creating new ones:

```python
# Good - One client for multiple operations
client = ZerobyteClient(url="...", username="...", password="...")
volumes = client.volumes.list()
repos = client.repositories.list(1)

# Bad - Don't create new clients repeatedly
for i in range(10):
    client = ZerobyteClient(...)  # This logs in 10 times!
```

### 3. Retention Policies

Design retention policies carefully:

```python
retention = {
    "keepLast": 7,      # Always keep last 7 (for quick recovery)
    "keepDaily": 30,    # Keep daily for last month
    "keepWeekly": 12,   # Keep weekly for ~3 months
    "keepMonthly": 24,  # Keep monthly for 2 years
    "keepYearly": 5     # Keep yearly for 5 years
}
```

### 4. Backup Scheduling

Use cron expressions wisely:

```python
schedules = {
    "hourly": "0 * * * *",           # Every hour
    "daily_2am": "0 2 * * *",        # Every day at 2 AM
    "weekly_sunday": "0 3 * * 0",    # Every Sunday at 3 AM
    "monthly_1st": "0 4 1 * *",      # 1st of month at 4 AM
}
```

### 5. Testing Backups

Regularly verify your backups work:

```python
# 1. Create test restore directory
# 2. Restore a small file
# 3. Verify contents
# 4. Clean up

snapshot = snapshots[0]  # Most recent
client.snapshots.restore(
    volume_id, repo_id, snapshot['id'],
    restore_data={
        "target": "/tmp/restore-test",
        "include": ["/etc/hostname"]  # Small file
    }
)
# Verify /tmp/restore-test/etc/hostname exists and is correct
```

## Next Steps

1. **Explore Examples**
   - Check the `examples/` directory for more code samples
   - Run `python examples/basic_usage.py`

2. **Read API Reference**
   - See `API_REFERENCE.md` for complete API documentation

3. **Automate Your Workflows**
   - Create scripts for common tasks
   - Use cron or systemd timers for scheduling

4. **Monitor and Maintain**
   - Set up notifications
   - Regularly check backup status
   - Test restores periodically

## Getting Help

- **Documentation**: See README.md and API_REFERENCE.md
- **Examples**: Check examples/ directory
- **Issues**: Report on GitHub
- **API Spec**: Refer to swagger.json

Happy backing up! 🎉
