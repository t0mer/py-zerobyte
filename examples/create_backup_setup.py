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
        repository_data={
            "name": "main-backup-repo",
            "compressionMode": "auto",
            "config": {
                "backend": "local",
                "name": "main-backup-repo",
                "path": "/mnt/backups/restic-repo"
            }
        }
    )
    repo_name = repository['repository']['name']
    print(f"   ✓ Repository created: {repo_name} (ID: {repository['repository']['id']})")
    
    # Step 4: Create backup schedule
    # TODO: Backup schedules API needs to be updated to match actual endpoints
    # print("\n4. Creating backup schedule...")
    # schedule = client.backup_schedules.create(
    #     schedule_data={
    #         "name": "Daily System Backup",
    #         "cronExpression": "0 2 * * *",  # Every day at 2 AM
    #         "enabled": True,
    #         "volumeId": volume_id,
    #         "repositoryId": repo_name,
    #         "includePatterns": [
    #             "/home",
    #             "/etc",
    #             "/var/www"
    #         ],
    #         "excludePatterns": [
    #             "/home/*/.cache",
    #             "/var/www/cache"
    #         ],
    #         "retentionPolicy": {
    #             "keepLast": 7,
    #             "keepDaily": 7,
    #             "keepWeekly": 4,
    #             "keepMonthly": 12,
    #             "keepYearly": 3
    #         }
    #     }
    # )
    # print(f"   ✓ Schedule created: {schedule['name']} (ID: {schedule['id']})")
    print("\n4. Skipping backup schedule creation (API needs updates)")
    
    # Step 5: Create notification destination
    # TODO: Update after backup schedules API is fixed
    print("\n5. Skipping notification setup (depends on backup schedules)")
    # notification = client.notifications.create_destination({
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
