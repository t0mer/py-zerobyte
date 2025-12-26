"""
Example: Monitor backup status and health.

This example demonstrates:
- Checking volume health
- Listing backup schedules and their status
- Viewing recent snapshots
- Generating a backup status report
"""

from py_zerobyte import ZerobyteClient
from datetime import datetime

def main():
    # Initialize client
    client = ZerobyteClient(
        url="https://svcbck.cloudguard.co.il/",
        username="tomer",
        password="T0m#r!2405-77"
    )
    print("Backup System Status Report")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get system info
    system_info = client.system.get_info()
    print(f"Zerobyte Version: {system_info.get('version', 'Unknown')}")
    print()
    
    # List all volumes
    volumes = client.volumes.list()
    print(f"Total Volumes: {len(volumes)}\n")
    
    for volume in volumes:
        volume_id = volume['id']
        print("-" * 80)
        print(f"Volume: {volume['name']} (ID: {volume_id})")
        print(f"  Device: {volume.get('device', 'N/A')}")
        print(f"  Mount Point: {volume.get('mountPoint', 'N/A')}")
        print(f"  Mounted: {'Yes' if volume.get('mounted') else 'No'}")
        print(f"  Auto Remount: {'Yes' if volume.get('autoRemount') else 'No'}")
        
        # Check volume health
        try:
            health = client.volumes.health_check(volume_id)
            print(f"  Health: {health.get('status', 'Unknown')}")
        except Exception as e:
            print(f"  Health: Unable to check ({e})")
        
        # List repositories for this volume
        repositories = client.repositories.list(volume_id)
        print(f"\n  Repositories: {len(repositories)}")
        
        for repo in repositories:
            repo_name = repo['name']
            print(f"\n    • {repo_name} (ID: {repo['id']})")
            print(f"      Type: {repo.get('type', 'Unknown')}")
            
            # List snapshots for this repository
            try:
                snapshots = client.snapshots.list(repo_name)
                print(f"      Snapshots: {len(snapshots)}")
                
                if snapshots:
                    latest = snapshots[0]
                    print(f"      Latest Snapshot: {latest.get('time', 'Unknown')}")
                    print(f"      Snapshot ID: {latest.get('short_id', 'Unknown')}")
            except Exception as e:
                print(f"      Snapshots: Unable to fetch ({e})")
            
            # TODO: Backup schedules API needs updates
            # # List backup schedules for this repository
            # try:
            #     schedules = client.backup_schedules.list_all()
            #     # Filter for this volume
            #     volume_schedules = [s for s in schedules if s.get('volumeId') == volume_id]
            #     print(f"      Backup Schedules: {len(volume_schedules)}")
            #     
            #     for schedule in volume_schedules:
            #         status_icon = "✓" if schedule.get('enabled') else "✗"
            #         print(f"\n        {status_icon} {schedule['name']} (ID: {schedule['id']})")
            #         print(f"          Schedule: {schedule.get('cronExpression', 'N/A')}")
            #         print(f"          Enabled: {'Yes' if schedule.get('enabled') else 'No'}")
            # except Exception as e:
            #     print(f"      Schedules: Unable to fetch ({e})")
        
        print()
    
    # Summary statistics
    print("="*80)
    print("Summary")
    print("="*80)
    
    total_repos = 0
    total_schedules = 0
    total_snapshots = 0
    enabled_schedules = 0
    
    for volume in volumes:
        volume_id = volume['id']
        repos = client.repositories.list(volume_id)
        total_repos += len(repos)
        
        for repo in repos:
            repo_id = repo['id']
            
            try:
                snapshots = client.snapshots.list(volume_id, repo_id)
                total_snapshots += len(snapshots)
            except:
                pass
            
            try:
                schedules = client.backup_schedules.list(volume_id, repo_id)
                total_schedules += len(schedules)
                enabled_schedules += sum(1 for s in schedules if s.get('enabled'))
            except:
                pass
    
    print(f"Total Volumes: {len(volumes)}")
    print(f"Total Repositories: {total_repos}")
    print(f"Total Backup Schedules: {total_schedules}")
    print(f"  - Enabled: {enabled_schedules}")
    print(f"  - Disabled: {total_schedules - enabled_schedules}")
    print(f"Total Snapshots: {total_snapshots}")
    print()

if __name__ == "__main__":
    main()
