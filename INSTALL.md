# Zerobyte SDK Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip package manager

## Installation Methods

### Method 1: Install from PyPI (Recommended)

Once published to PyPI, you can install using pip:

```bash
pip install py-zerobyte
```

### Method 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/t0mer/py-zerobyte.git
cd py-zerobyte
```

2. Install in development mode:
```bash
pip install -e .
```

Or install directly:
```bash
pip install .
```

### Method 3: Install from GitHub

```bash
pip install git+https://github.com/t0mer/py-zerobyte.git
```

## Verify Installation

After installation, verify it works:

```bash
python -c "from py_zerobyte import ZerobyteClient; print('Zerobyte SDK installed successfully!')"
```

## Development Installation

For development with testing tools:

```bash
pip install -e ".[dev]"
```

This installs additional development dependencies:
- pytest (for testing)
- pytest-cov (for coverage)
- black (for code formatting)
- flake8 (for linting)

## Quick Start

After installation, try this quick test:

```python
from py_zerobyte import ZerobyteClient

# Initialize client
client = ZerobyteClient(
    url="http://localhost:4096",
    username="your-username",
    password="your-password"
)

# Get user info
user = client.auth.get_me()
print(f"Connected as: {user['user']['username']}")

# List volumes
volumes = client.volumes.list()
print(f"Found {len(volumes)} volume(s)")
```

## Troubleshooting

### ImportError: No module named 'py_zerobyte'

Make sure the package is installed:
```bash
pip list | grep zerobyte
```

If not found, reinstall:
```bash
pip install py-zerobyte
```

### Connection Issues

If you get connection errors, verify:
1. Zerobyte API server is running
2. URL is correct (include http:// or https://)
3. Port is accessible
4. Credentials are correct

### SSL Certificate Issues

If using HTTPS with self-signed certificates, you may need to disable SSL verification (not recommended for production):

```python
import requests
# Disable SSL warnings
requests.packages.urllib3.disable_warnings()
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade py-zerobyte
```

## Uninstallation

To remove the SDK:

```bash
pip uninstall py-zerobyte
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/t0mer/py-zerobyte/issues
- Documentation: https://github.com/t0mer/py-zerobyte
