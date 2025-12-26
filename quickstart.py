#!/usr/bin/env python3
"""
Quick start script for Zerobyte SDK.

This script demonstrates the basic workflow:
1. Connect to Zerobyte API
2. Create a volume
3. Create a repository
4. Set up a backup schedule
"""

from py_zerobyte import ZerobyteClient

# Configuration - Update these values
API_URL = "http://localhost:4096"
USERNAME = "admin"
PASSWORD = "your-password"

VOLUME_CONFIG = {
    "name": "my-backup-volume",
    "device": "/dev/sdb1",
    "mountPoint": "/mnt/backup",
    "filesystem": "ext4",
    "autoRemount": True,
    "readonly": False,
    "options": []
}

REPOSITORY_CONFIG = {
    "name": "my-repository",
    "type": "local",
    "config": {
        "path": "/mnt/backup/restic-repo"
    }
}

SCHEDULE_CONFIG = {
    "name": "Daily Backup",
    "schedule": "0 2 * * *",  # Every day at 2 AM
    "enabled": True,
    "backupPaths": ["/home", "/etc"],
    "excludePaths": ["/home/*/.cache"],
    "retention": {
        "keepLast": 7,
        "keepDaily": 7,
        "keepWeekly": 4,
        "keepMonthly": 12
    }
}


def main():
    print("Zerobyte SDK Quick Start")
    print("=" * 60)
    
    # Step 1: Connect
    print("\n1. Connecting to Zerobyte API...")
    client = ZerobyteClient(
        url=API_URL,
        username=USERNAME,
        password=PASSWORD
    )
    user = client.auth.get_me()
    print(f"   ✓ Connected as: {user['user']['username']}")
    
    # Step 2: Create Volume
    print("\n2. Creating volume...")
    volume = client.volumes.create(VOLUME_CONFIG)
    volume_id = volume['id']
    print(f"   ✓ Volume created: {volume['name']} (ID: {volume_id})")
    
    # Step 3: Mount Volume
    print("\n3. Mounting volume...")
    client.volumes.mount(volume_id)
    print("   ✓ Volume mounted")
    
    # Step 4: Create Repository
    print("\n4. Creating repository...")
    repository = client.repositories.create(volume_id, REPOSITORY_CONFIG)
    repo_id = repository['id']
    print(f"   ✓ Repository created: {repository['name']} (ID: {repo_id})")
    
    # Step 5: Create Backup Schedule
    print("\n5. Creating backup schedule...")
    schedule = client.backup_schedules.create(
        volume_id,
        repo_id,
        SCHEDULE_CONFIG
    )
    schedule_id = schedule['id']
    print(f"   ✓ Schedule created: {schedule['name']} (ID: {schedule_id})")
    
    # Step 6: Run Initial Backup
    print("\n6. Running initial backup...")
    client.backup_schedules.run_now(volume_id, repo_id, schedule_id)
    print("   ✓ Backup started")
    
    print("\n" + "=" * 60)
    print("Quick Start Complete!")
    print("=" * 60)
    print(f"\nYour backup system is now configured:")
    print(f"  - Volume ID: {volume_id}")
    print(f"  - Repository ID: {repo_id}")
    print(f"  - Schedule ID: {schedule_id}")
    print(f"\nBackups will run daily at 2:00 AM")
    print(f"Backing up: {', '.join(SCHEDULE_CONFIG['backupPaths'])}")
    print(f"\nTo view snapshots:")
    print(f"  snapshots = client.snapshots.list({volume_id}, {repo_id})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure to update the configuration values at the top of this script!")
