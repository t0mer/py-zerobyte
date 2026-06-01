# Installation Guide — Zerobyte SDK

## Prerequisites

- Python 3.7 or higher
- pip

## Install from PyPI (recommended)

```bash
pip install py-zerobyte
```

## Install from Source

```bash
git clone https://github.com/t0mer/py-zerobyte.git
cd py-zerobyte
pip install .
```

## Install in Development Mode

```bash
git clone https://github.com/t0mer/py-zerobyte.git
cd py-zerobyte
pip install -e ".[dev]"
```

Dev extras include: `pytest`, `pytest-cov`, `black`, `flake8`.

## Install from GitHub (latest unreleased)

```bash
pip install git+https://github.com/t0mer/py-zerobyte.git
```

## Verify Installation

```bash
python -c "from py_zerobyte import ZerobyteClient; print('OK')"
```

## Quick Connection Test

```python
from py_zerobyte import ZerobyteClient

client = ZerobyteClient(
    url="http://localhost:4096",
    username="your-username",
    password="your-password"
)

session = client.auth.get_me()
print(f"Connected as: {session['user']['username']}")

volumes = client.volumes.list()
print(f"Volumes: {len(volumes)}")
```

## Upgrade

```bash
pip install --upgrade py-zerobyte
```

## Uninstall

```bash
pip uninstall py-zerobyte
```

---

## Troubleshooting

### `ImportError: No module named 'py_zerobyte'`

```bash
pip list | grep zerobyte
# If missing:
pip install py-zerobyte
```

### `AuthenticationError` on init

- Confirm the server is reachable: `curl http://localhost:4096/api/v1/auth/status`
- Verify username and password are correct
- Check that the URL scheme and port are correct

### `ConnectionError` / `requests.exceptions.ConnectionError`

- Make sure the Zerobyte server is running
- Confirm the `url` includes the scheme and port: `http://host:4096`
- Check firewall / network rules if connecting to a remote host

### SSL certificate errors (self-signed certs)

The SDK uses `requests` which verifies TLS certificates by default. **Do not disable verification** — doing so exposes credentials to man-in-the-middle attacks.

Instead, add your CA certificate to the trust store:

```bash
# Debian / Ubuntu
sudo cp my-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# RHEL / Fedora
sudo cp my-ca.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

Or point `requests` at your CA bundle directly:

```python
client = ZerobyteClient(url="https://...", username="...", password="...")
client.session.verify = "/path/to/ca-bundle.crt"
```

For development, consider using a properly-issued certificate from [Let's Encrypt](https://letsencrypt.org/) or a local CA like [mkcert](https://github.com/FiloSottile/mkcert) instead of a self-signed cert.

## Support

- Issues: https://github.com/t0mer/py-zerobyte/issues
- Documentation: https://github.com/t0mer/py-zerobyte
