# Zerobyte SDK Examples

This directory contains practical examples demonstrating various use cases for the Zerobyte SDK.

## Examples

### 1. basic_usage.py
Basic example showing how to:
- Initialize the client
- Get user information
- List volumes and repositories
- Check system status

**Run:**
```bash
python basic_usage.py
```

### 2. create_backup_setup.py
Complete backup setup example:
- Create and mount a volume
- Create a backup repository
- Configure a backup schedule with retention policy
- Set up email notifications
- Run initial backup

**Run:**
```bash
python create_backup_setup.py
```

### 3. restore_snapshot.py
Snapshot restore example:
- List available snapshots
- Browse snapshot contents
- Restore specific files/directories from a snapshot

**Run:**
```bash
python restore_snapshot.py
```

### 4. manage_notifications.py
Notification management example:
- Create email, Slack, and webhook notification destinations
- Test notifications
- Update notification settings

**Run:**
```bash
python manage_notifications.py
```

### 5. monitor_status.py
System monitoring and reporting:
- Check volume health
- List all backup schedules and their status
- View recent snapshots
- Generate comprehensive status report

**Run:**
```bash
python monitor_status.py
```

## Configuration

Before running these examples, make sure to update the connection parameters:

```python
client = ZerobyteClient(
    url="http://localhost:4096",  # Your Zerobyte API URL
    username="admin",              # Your username
    password="your-password"       # Your password
)
```

Also update any volume/repository IDs and file paths to match your environment.

## Requirements

Install the SDK first:

```bash
pip install py-zerobyte
```

Or if running from source:

```bash
cd ..
pip install -e .
```
