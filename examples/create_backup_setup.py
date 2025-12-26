"""
Example: Create a complete backup setup.

This example demonstrates:
- Creating a volume
- Mounting the volume
- Creating a repository
- Setting up a backup schedule with retention policy
- Configuring notifications
"""

from py_zerobyte import ZerobyteClient

def main():
    # Initialize client
    client = ZerobyteClient(
        url="http://localhost:4096",
        username="admin",
        password="your-password"
    )
    
    print("Setting up backup infrastructure...\n")
    
    # Step 1: Create a volume
    print("1. Creating volume...")
    volume = client.volumes.create({
        "name": "backup-storage",
        "device": "/dev/sdb1",
        "mountPoint": "/mnt/backups",
        "filesystem": "ext4",
        "autoRemount": True,
        "readonly": False,
        "options": []
    })
    volume_id = volume['id']
    print(f"   ✓ Volume created: {volume['name']} (ID: {volume_id})")
    
    # Step 2: Mount the volume
    print("\n2. Mounting volume...")
    client.volumes.mount(volume_id)
    print("   ✓ Volume mounted successfully")
    
    # Step 3: Create a repository
    print("\n3. Creating backup repository...")
    repository = client.repositories.create(
        volume_id=volume_id,
        repository_data={
            "name": "main-backup-repo",
            "type": "local",
            "config": {
                "path": "/mnt/backups/restic-repo"
            }
        }
    )
    repo_id = repository['id']
    print(f"   ✓ Repository created: {repository['name']} (ID: {repo_id})")
    
    # Step 4: Create backup schedule
    print("\n4. Creating backup schedule...")
    schedule = client.backup_schedules.create(
        volume_id=volume_id,
        repository_id=repo_id,
        schedule_data={
            "name": "Daily System Backup",
            "schedule": "0 2 * * *",  # Every day at 2 AM
            "enabled": True,
            "backupPaths": [
                "/home",
                "/etc",
                "/var/www"
            ],
            "excludePaths": [
                "/home/*/.cache",
                "/var/www/cache"
            ],
            "retention": {
                "keepLast": 7,      # Keep last 7 snapshots
                "keepDaily": 7,     # Keep daily backups for 7 days
                "keepWeekly": 4,    # Keep weekly backups for 4 weeks
                "keepMonthly": 12,  # Keep monthly backups for 12 months
                "keepYearly": 3     # Keep yearly backups for 3 years
            },
            "tags": ["daily", "system", "automated"]
        }
    )
    schedule_id = schedule['id']
    print(f"   ✓ Schedule created: {schedule['name']} (ID: {schedule_id})")
    print(f"   Schedule: {schedule['schedule']}")
    
    # Step 5: Create notification destination
    print("\n5. Setting up email notifications...")
    notification = client.notifications.create_destination({
        "name": "Admin Email Alerts",
        "type": "email",
        "config": {
            "to": "admin@example.com",
            "from": "backup@example.com",
            "smtpHost": "smtp.gmail.com",
            "smtpPort": 587,
            "username": "backup@example.com",
            "password": "your-app-password"
        }
    })
    notification_id = notification['id']
    print(f"   ✓ Notification destination created: {notification['name']}")
    
    # Step 6: Link notifications to schedule
    print("\n6. Configuring backup notifications...")
    client.backup_schedules.update_notifications(
        volume_id=volume_id,
        repository_id=repo_id,
        schedule_id=schedule_id,
        notifications_data={
            "onSuccess": True,
            "onFailure": True,
            "destinations": [notification_id]
        }
    )
    print("   ✓ Notifications configured for success and failure")
    
    # Step 7: Run initial backup
    print("\n7. Running initial backup...")
    client.backup_schedules.run_now(
        volume_id=volume_id,
        repository_id=repo_id,
        schedule_id=schedule_id
    )
    print("   ✓ Initial backup started")
    
    print("\n" + "="*50)
    print("Backup setup completed successfully!")
    print("="*50)
    print(f"\nVolume ID: {volume_id}")
    print(f"Repository ID: {repo_id}")
    print(f"Schedule ID: {schedule_id}")
    print(f"\nBackup will run daily at 2:00 AM")
    print(f"Notifications will be sent to: admin@example.com")

if __name__ == "__main__":
    main()
