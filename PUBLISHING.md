# Publishing Zerobyte SDK to PyPI

This guide explains how to publish the Zerobyte SDK to PyPI so users can install it with `pip install py-zerobyte`.

## Prerequisites

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Create an account
   - Verify your email

2. **Create TestPyPI Account** (for testing)
   - Go to https://test.pypi.org/account/register/
   - Create an account (can use same credentials)

3. **Install Build Tools**
   ```bash
   pip install --upgrade build twine
   ```

## Step-by-Step Publishing

### 1. Prepare the Package

Ensure all files are ready:
```bash
cd /opt/dev/py-zerobyte

# Check structure
tree -L 2

# Expected structure:
# .
# ├── py_zerobyte/
# │   ├── __init__.py
# │   ├── auth.py
# │   ├── backup_schedules.py
# │   ├── client.py
# │   ├── exceptions.py
# │   ├── notifications.py
# │   ├── repositories.py
# │   ├── snapshots.py
# │   ├── system.py
# │   └── volumes.py
# ├── examples/
# ├── tests/
# ├── setup.py
# ├── pyproject.toml
# ├── README.md
# ├── LICENSE
# └── MANIFEST.in
```

### 2. Update Version (if needed)

Edit these files to update version number:
- `setup.py` (line with `version=`)
- `pyproject.toml` (line with `version =`)
- `py_zerobyte/__init__.py` (line with `__version__ =`)

### 3. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info
```

### 4. Build the Package

```bash
python -m build
```

This creates:
- `dist/py_zerobyte-1.0.0.tar.gz` (source distribution)
- `dist/py_zerobyte-1.0.0-py3-none-any.whl` (wheel distribution)

### 5. Test on TestPyPI (Recommended)

First, upload to TestPyPI to verify everything works:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
```

Enter your TestPyPI username and password when prompted.

**Alternative: Use API Token**
1. Go to https://test.pypi.org/manage/account/token/
2. Create a new API token
3. Create `~/.pypirc`:
   ```ini
   [testpypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmc...  # Your token
   ```

Then upload:
```bash
python -m twine upload --repository testpypi dist/*
```

### 6. Test Installation from TestPyPI

```bash
# Create a virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps py-zerobyte

# Install dependencies
pip install requests

# Test it
python -c "from py_zerobyte import ZerobyteClient; print('Success!')"
```

### 7. Upload to Production PyPI

Once testing is successful:

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

Enter your PyPI username and password (or use API token from https://pypi.org/manage/account/token/).

### 8. Verify Installation

```bash
# In a fresh environment
pip install py-zerobyte

# Test
python -c "from py_zerobyte import ZerobyteClient; print('Installed successfully!')"
```

## Using API Tokens (Recommended)

Instead of using username/password, use API tokens:

1. **Create API Token:**
   - Go to https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Enter token name (e.g., "py-zerobyte")
   - Set scope (entire account or specific project)
   - Copy the token (you'll only see it once!)

2. **Configure `.pypirc`:**
   Create/edit `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmc...  # Your token here

   [testpypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmc...  # Your TestPyPI token
   ```

3. **Upload:**
   ```bash
   python -m twine upload dist/*
   ```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python -m twine upload dist/*
```

Add your PyPI API token to GitHub Secrets:
1. Go to repository Settings → Secrets → Actions
2. Add new secret named `PYPI_API_TOKEN`
3. Paste your PyPI token

## Updating a Package

When releasing a new version:

1. **Update version numbers** in:
   - `setup.py`
   - `pyproject.toml`
- `py_zerobyte/__init__.py`

3. **Clean and rebuild:**
   ```bash
   rm -rf build/ dist/ *.egg-info
   python -m build
   ```

4. **Upload new version:**
   ```bash
   python -m twine upload dist/*
   ```

## Troubleshooting

### Error: "File already exists"
- You're trying to upload a version that already exists
- PyPI doesn't allow replacing existing versions
- Increment the version number and rebuild

### Error: "Invalid distribution"
- Check that all required files exist (README.md, LICENSE, etc.)
- Ensure setup.py and pyproject.toml are properly formatted
- Verify MANIFEST.in includes all necessary files

### Error: "Package name not available"
- The package name is already taken (e.g., "zerobyte-sdk" might be taken, so we use "py-zerobyte")
- Choose a different name in setup.py and pyproject.toml
- Search PyPI first: https://pypi.org/search/

### Error: "Long description rendering failed"
- Your README.md has syntax errors
- Test locally: `python -m readme_renderer README.md`
- Fix any Markdown syntax issues

## Best Practices

1. **Always test on TestPyPI first**
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Keep a CHANGELOG.md**
4. **Tag releases in Git:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
5. **Write clear release notes**
6. **Test installation in clean environment**

## Resources

- PyPI: https://pypi.org/
- TestPyPI: https://test.pypi.org/
- Packaging Guide: https://packaging.python.org/
- Twine: https://twine.readthedocs.io/
- Build: https://pypa-build.readthedocs.io/
