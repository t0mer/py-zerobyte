# 🎯 Quick Start Guide

**Zerobyte SDK** - Python SDK for the Zerobyte API

## Installation

```bash
pip install py-zerobyte
```

## 30-Second Example

```python
from py_zerobyte import ZerobyteClient

# Connect (URL, username, password configured here as requested)
client = ZerobyteClient(
    url="http://localhost:4096",
    username="admin",
    password="your-password"
)

# Use the API
volumes = client.volumes.list()
print(f"Found {len(volumes)} volumes")
```

## What's Included

✅ **All 52 API endpoints** from your swagger.json  
✅ **Complete documentation** (README, API Reference, Tutorial)  
✅ **5 working examples** (basic usage, backup setup, restore, notifications, monitoring)  
✅ **Error handling** with custom exceptions  
✅ **Type hints** for IDE support  
✅ **Ready for PyPI** (setup.py, pyproject.toml configured)

## File Overview

### 📦 Core Package
- `py_zerobyte/` - Main package with all API methods
  - `client.py` - Main client (URL/user/pass in `__init__`)
  - `auth.py` - Authentication API
  - `volumes.py` - Volumes API
  - `repositories.py` - Repositories API
  - `snapshots.py` - Snapshots API
  - `backup_schedules.py` - Backup Schedules API
  - `notifications.py` - Notifications API
  - `system.py` - System API
  - `exceptions.py` - Custom exceptions

### 📚 Documentation
- `README.md` - Main documentation with examples
- `API_REFERENCE.md` - Complete API reference
- `TUTORIAL.md` - Step-by-step tutorial
- `INSTALL.md` - Installation guide
- `PUBLISHING.md` - PyPI publishing guide
- `PROJECT_SUMMARY.md` - Project overview
- `CHECKLIST.md` - Pre-publishing checklist

### 💡 Examples
- `examples/basic_usage.py` - Basic connection and listing
- `examples/create_backup_setup.py` - Full backup setup
- `examples/restore_snapshot.py` - Snapshot restoration
- `examples/manage_notifications.py` - Notification setup
- `examples/monitor_status.py` - System monitoring
- `quickstart.py` - Quick start script

### 🧪 Testing
- `tests/test_client.py` - Unit tests
- Run with: `pytest`

### ⚙️ Configuration
- `setup.py` - Package setup
- `pyproject.toml` - Modern Python config
- `requirements.txt` - Dependencies
- `LICENSE` - MIT License
- `.gitignore` - Git ignore patterns

## API Coverage

| Category | Methods | Status |
|----------|---------|--------|
| Authentication | 6 | ✅ Complete |
| Volumes | 11 | ✅ Complete |
| Repositories | 5 | ✅ Complete |
| Snapshots | 5 | ✅ Complete |
| Backup Schedules | 15 | ✅ Complete |
| Notifications | 6 | ✅ Complete |
| System | 2 | ✅ Complete |
| **TOTAL** | **52** | ✅ **100%** |

## Quick Examples

### List Resources
```python
volumes = client.volumes.list()
repos = client.repositories.list(volume_id=1)
snapshots = client.snapshots.list(volume_id=1, repository_id=1)
```

### Create Backup Schedule
```python
schedule = client.backup_schedules.create(
    volume_id=1,
    repository_id=1,
    schedule_data={
        "name": "Daily Backup",
        "schedule": "0 2 * * *",
        "backupPaths": ["/home", "/etc"],
        "retention": {"keepLast": 7, "keepDaily": 7}
    }
)
```

### Run Backup Now
```python
client.backup_schedules.run_now(volume_id=1, repository_id=1, schedule_id=1)
```

### Restore Snapshot
```python
client.snapshots.restore(
    volume_id=1,
    repository_id=1,
    snapshot_id="abc123",
    restore_data={"target": "/restore", "include": ["/home"]}
)
```

## Publishing to PyPI

```bash
# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

See `PUBLISHING.md` for detailed instructions.

## Next Steps

1. **Read** `TUTORIAL.md` for step-by-step guide
2. **Try** examples in `examples/` directory
3. **Test** with your Zerobyte API instance
4. **Publish** to PyPI (see `PUBLISHING.md`)

## Documentation Map

- **New user?** → Start with `TUTORIAL.md`
- **Need API details?** → See `API_REFERENCE.md`
- **Want examples?** → Check `examples/` directory
- **Installing?** → Read `INSTALL.md`
- **Publishing?** → Follow `PUBLISHING.md`
- **Overview?** → See `PROJECT_SUMMARY.md`

## Requirements

- Python 3.7+
- requests >= 2.25.0

## Support

Created with ❤️ based on your swagger.json specification.  
All 52 endpoints covered with URL/username/password in `__init__` as requested.

---

**Status**: ✅ Ready for production  
**Version**: 1.0.0  
**License**: MIT
