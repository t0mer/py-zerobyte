# Pre-Publishing Checklist

Use this checklist before publishing the Zerobyte SDK to PyPI.

## Code Quality

- [x] All API endpoints from swagger.json implemented
- [x] URL, username, password configured in `__init__`
- [x] Error handling implemented
- [x] Type hints added
- [x] Docstrings for all public methods
- [ ] Code formatted with black: `black py_zerobyte/`
- [ ] No linting errors: `flake8 py_zerobyte/`
- [ ] Tests pass: `pytest tests/`

## Documentation

- [x] README.md complete with examples
- [x] API_REFERENCE.md complete
- [x] INSTALL.md with installation instructions
- [x] PUBLISHING.md with publishing guide
- [x] Example scripts in examples/
- [x] LICENSE file present
- [x] PROJECT_SUMMARY.md created

## Package Configuration

- [x] setup.py configured correctly
- [x] pyproject.toml configured correctly
- [x] requirements.txt lists all dependencies
- [x] MANIFEST.in includes necessary files
- [x] .gitignore configured
- [x] Version numbers consistent across files:
  - [ ] setup.py
  - [ ] pyproject.toml
  - [ ] py_zerobyte/__init__.py

## Testing

- [ ] Test with actual Zerobyte API instance
- [ ] Verify all endpoints work correctly
- [ ] Test error handling
- [ ] Test authentication flow
- [ ] Run example scripts successfully

## Pre-Publishing Steps

1. **Update Package Name (if needed)**
   - [x] Package name set to "py-zerobyte"
   - [x] Updated in setup.py
   - [x] Updated in pyproject.toml
   - [x] Updated in README.md

2. **Clean Build**
   ```bash
   rm -rf build/ dist/ *.egg-info
   ```

3. **Build Package**
   ```bash
   python -m build
   ```
   - [ ] Build completes without errors
   - [ ] Both .tar.gz and .whl files created

4. **Check Package**
   ```bash
   twine check dist/*
   ```
   - [ ] All checks pass

5. **Test Upload to TestPyPI**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
   - [ ] Upload successful

6. **Test Installation from TestPyPI**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ py-zerobyte
   ```
   - [ ] Installation successful
   - [ ] Import works: `from py_zerobyte import ZerobyteClient`
   - [ ] Basic functionality works

## Publishing

7. **Upload to Production PyPI**
   ```bash
   python -m twine upload dist/*
   ```
   - [ ] Upload successful

8. **Test Installation from PyPI**
   ```bash
   pip install py-zerobyte
   ```
   - [ ] Installation successful
   - [ ] All functionality works

## Post-Publishing

9. **Create Git Repository** (if not done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit - v1.0.0"
   git tag -a v1.0.0 -m "Release version 1.0.0"
   ```

10. **Push to GitHub**
    - [ ] Create repository on GitHub
    - [ ] Push code
    - [ ] Push tags
    - [ ] Update repository URL in setup.py and pyproject.toml

11. **Documentation**
    - [ ] Update GitHub repository description
    - [ ] Add topics/tags to repository
    - [ ] Create release notes on GitHub
    - [ ] Link to PyPI package in README

12. **Announce**
    - [ ] Share on relevant forums/communities
    - [ ] Update project documentation
    - [ ] Notify stakeholders

## Common Issues to Check

- [ ] All imports work correctly
- [ ] No circular imports
- [ ] No hardcoded credentials in code
- [ ] No absolute file paths in code
- [ ] README renders correctly on PyPI
- [ ] All example scripts have updated configuration instructions
- [ ] License year is correct
- [ ] Author/maintainer information is correct

## Final Verification Commands

Run these before publishing:

```bash
# Check package structure
tree -L 3

# Run tests
pytest

# Format code
black py_zerobyte/

# Check linting
flake8 py_zerobyte/

# Check setup.py
python setup.py check

# Build
python -m build

# Check distribution
twine check dist/*

# Test import
python -c "from py_zerobyte import ZerobyteClient; print('OK')"
```

## Version Numbers to Update

When releasing a new version, update these files:

1. `setup.py` - line with `version=`
2. `pyproject.toml` - line with `version =`
3. `py_zerobyte/__init__.py` - line with `__version__ =`

All three must match!

## Support Checklist

- [ ] Issue template created on GitHub
- [ ] Contributing guidelines created
- [ ] Code of conduct added
- [ ] Support documentation available
- [ ] Contact information updated

---

**Remember:** You can only upload each version once to PyPI. Test thoroughly on TestPyPI first!
