"""
Example: Restore from a snapshot.

This example demonstrates:
- Listing available snapshots
- Selecting a snapshot to restore
- Restoring files from a snapshot
"""

from py_zerobyte import ZerobyteClient
from datetime import datetime

def main():
    # Initialize client
    client = ZerobyteClient(
        url="http://localhost:4096",
        username="admin",
        password="your-password"
    )
    
    # Configuration
    volume_id = 1
    repository_id = 1
    restore_target = "/restore"
    
    print("Snapshot Restore Tool\n")
    
    # Step 1: List available snapshots
    print("1. Fetching available snapshots...")
    snapshots = client.snapshots.list(
        volume_id=volume_id,
        repository_id=repository_id
    )
    
    if not snapshots:
        print("   ✗ No snapshots found")
        return
    
    print(f"   ✓ Found {len(snapshots)} snapshots\n")
    
    # Display snapshots
    print("Available Snapshots:")
    print("-" * 80)
    for i, snapshot in enumerate(snapshots, 1):
        snapshot_time = snapshot.get('time', 'Unknown')
        snapshot_id = snapshot.get('id', 'Unknown')
        tags = ', '.join(snapshot.get('tags', []))
        print(f"{i}. {snapshot_id}")
        print(f"   Time: {snapshot_time}")
        print(f"   Tags: {tags if tags else 'None'}")
        print()
    
    # For this example, we'll restore the most recent snapshot
    latest_snapshot = snapshots[0]
    snapshot_id = latest_snapshot['id']
    
    print(f"Selected snapshot: {snapshot_id}")
    print(f"Created: {latest_snapshot.get('time', 'Unknown')}\n")
    
    # Step 2: List files in the snapshot
    print("2. Listing files in snapshot...")
    files = client.snapshots.list_files(
        volume_id=volume_id,
        repository_id=repository_id,
        snapshot_id=snapshot_id,
        path="/"
    )
    
    print(f"   ✓ Snapshot contains files\n")
    
    # Step 3: Restore the snapshot
    print(f"3. Restoring snapshot to {restore_target}...")
    
    restore_response = client.snapshots.restore(
        volume_id=volume_id,
        repository_id=repository_id,
        snapshot_id=snapshot_id,
        restore_data={
            "target": restore_target,
            "include": ["/home", "/etc"],  # Restore only specific paths
            "exclude": ["/home/*/.cache"]  # Exclude cache directories
        }
    )
    
    print("   ✓ Restore initiated successfully")
    
    print("\n" + "="*50)
    print("Restore Details:")
    print("="*50)
    print(f"Snapshot ID: {snapshot_id}")
    print(f"Restore Target: {restore_target}")
    print(f"Included Paths: /home, /etc")
    print(f"Excluded Paths: /home/*/.cache")
    print("\nThe restore operation is running in the background.")
    print("Check the logs for progress and completion status.")

if __name__ == "__main__":
    main()
