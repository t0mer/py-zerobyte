"""
Basic usage example for Zerobyte SDK.

This example demonstrates:
- Initializing the client
- Listing volumes and repositories
- Checking system status
"""

from py_zerobyte import ZerobyteClient, AuthenticationError

def main():
    # Initialize the client
    try:
        client = ZerobyteClient(
            url="http://localhost:4096",
            username="admin",
            password="your-password"
        )
        print("✓ Successfully connected to Zerobyte API")
    except AuthenticationError as e:
        print(f"✗ Authentication failed: {e}")
        return
    
    # Get current user information
    user = client.auth.get_me()
    print(f"\nLogged in as: {user['user']['username']}")
    
    # Get system information
    system_info = client.system.get_info()
    print(f"Zerobyte version: {system_info.get('version', 'Unknown')}")
    
    # List all volumes
    print("\n--- Volumes ---")
    volumes = client.volumes.list()
    if volumes:
        for volume in volumes:
            print(f"  • {volume['name']} - Mounted: {volume.get('mounted', False)}")
    else:
        print("  No volumes found")
    
    # List all repositories
    print("\n--- Repositories ---")
    repositories = client.repositories.list()
    if repositories:
        for repo in repositories:
            print(f"  • {repo['name']} ({repo.get('type', 'Unknown')})")
    else:
        print("  No repositories found")
        
    print("\n✓ Done!")

if __name__ == "__main__":
    main()
