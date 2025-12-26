"""
Example: Manage notification destinations.

This example demonstrates:
- Creating different types of notification destinations
- Testing notifications
- Managing notification configurations
"""

from py_zerobyte import ZerobyteClient

def main():
    # Initialize client
    client = ZerobyteClient(
        url="http://localhost:4096",
        username="admin",
        password="your-password"
    )
    
    print("Notification Destinations Setup\n")
    
    # Create Email notification
    print("1. Creating email notification destination...")
    email_dest = client.notifications.create_destination({
        "name": "Admin Email",
        "type": "email",
        "config": {
            "to": "admin@example.com",
            "from": "backup@example.com",
            "smtpHost": "smtp.gmail.com",
            "smtpPort": 587,
            "username": "backup@example.com",
            "password": "your-app-password",
            "useTLS": True
        }
    })
    print(f"   ✓ Created: {email_dest['name']} (ID: {email_dest['id']})")
    
    # Create Slack notification
    print("\n2. Creating Slack notification destination...")
    slack_dest = client.notifications.create_destination({
        "name": "Team Slack Channel",
        "type": "slack",
        "config": {
            "webhookUrl": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
            "channel": "#backups",
            "username": "Backup Bot"
        }
    })
    print(f"   ✓ Created: {slack_dest['name']} (ID: {slack_dest['id']})")
    
    # Create Webhook notification
    print("\n3. Creating webhook notification destination...")
    webhook_dest = client.notifications.create_destination({
        "name": "Custom Webhook",
        "type": "webhook",
        "config": {
            "url": "https://your-server.com/webhook",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer your-token",
                "Content-Type": "application/json"
            }
        }
    })
    print(f"   ✓ Created: {webhook_dest['name']} (ID: {webhook_dest['id']})")
    
    # Test email notification
    print("\n4. Testing email notification...")
    test_result = client.notifications.test_destination(email_dest['id'])
    if test_result.get('success'):
        print("   ✓ Test email sent successfully")
    else:
        print(f"   ✗ Test failed: {test_result.get('message', 'Unknown error')}")
    
    # List all notification destinations
    print("\n5. Listing all notification destinations...")
    all_destinations = client.notifications.list_destinations()
    print(f"   Total destinations: {len(all_destinations)}")
    for dest in all_destinations:
        print(f"   • {dest['name']} ({dest['type']}) - ID: {dest['id']}")
    
    # Update a notification destination
    print("\n6. Updating email notification...")
    updated_dest = client.notifications.update_destination(
        email_dest['id'],
        {
            "name": "Admin Email - Updated",
            "config": {
                "to": "admin@example.com,backup@example.com",  # Multiple recipients
                "from": "backup@example.com",
                "smtpHost": "smtp.gmail.com",
                "smtpPort": 587,
                "username": "backup@example.com",
                "password": "your-app-password",
                "useTLS": True
            }
        }
    )
    print(f"   ✓ Updated: {updated_dest['name']}")
    
    print("\n" + "="*50)
    print("Notification Setup Summary")
    print("="*50)
    print(f"Email Notification ID: {email_dest['id']}")
    print(f"Slack Notification ID: {slack_dest['id']}")
    print(f"Webhook Notification ID: {webhook_dest['id']}")
    print("\nYou can now use these notification IDs in your backup schedules.")

if __name__ == "__main__":
    main()
