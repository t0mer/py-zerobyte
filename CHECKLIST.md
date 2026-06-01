# Release Checklist — Zerobyte SDK

Use this checklist before publishing a new version to PyPI.

## Code Quality

- [ ] All tests pass: `pytest tests/`
- [ ] Code formatted: `black py_zerobyte/`
- [ ] No lint errors: `flake8 py_zerobyte/`
- [x] All 50 API endpoints implemented and verified against live instance
- [x] Type hints on all public methods
- [x] Docstrings on all public methods

## Version Bump

Update the version string in **all three** of these files (they must match):

- [ ] `py_zerobyte/__init__.py` — `__version__ = "X.Y.Z"`
- [ ] `setup.py` — `version="X.Y.Z"`
- [ ] `pyproject.toml` — `version = "X.Y.Z"`

## Documentation

- [ ] `README.md` — examples use current method signatures
- [ ] `API_REFERENCE.md` — all method signatures up to date
- [ ] `TUTORIAL.md` — walkthrough uses current API
- [ ] `QUICKSTART.md` — quick examples are correct
- [ ] `CHANGELOG` section in `README.md` updated

## API Correctness (re-verify after any server update)

- [ ] Auth: `client.auth.login(u, p)` succeeds
- [ ] Auth: `client.auth.get_me()` returns `{"session": ..., "user": ...}`
- [ ] Volumes: `client.volumes.list()` returns list; `shortId` field present
- [ ] Volumes: per-volume methods accept `shortId` string
- [ ] Repositories: `client.repositories.list()` returns list; `shortId` field present
- [ ] Repositories: `update()` uses PATCH
- [ ] Backup schedules: `create()` body includes `repositoryId` and `volumeId`
- [ ] Backup schedules: `update()` body includes `cronExpression` and `repositoryId`
- [ ] Notifications: `create_destination()` config dict has `type` field inside it
- [ ] System: `download_restic_password(password)` requires the account password

## Build

```bash
# Clean previous build artefacts
rm -rf build/ dist/ *.egg-info

# Build sdist + wheel
python -m build

# Verify the distribution
twine check dist/*
```

- [ ] Build completes without errors
- [ ] Both `.tar.gz` and `.whl` files present in `dist/`
- [ ] `twine check` passes with no errors or warnings

## TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ py-zerobyte
python -c "from py_zerobyte import ZerobyteClient; print('OK')"
```

- [ ] Upload to TestPyPI succeeds
- [ ] Install from TestPyPI succeeds
- [ ] Basic import works

## Production PyPI

```bash
python -m twine upload dist/*
pip install --upgrade py-zerobyte
python -c "from py_zerobyte import ZerobyteClient; print('OK')"
```

- [ ] Upload succeeds
- [ ] Install from PyPI succeeds

## Git

```bash
git tag -a v1.2.1 -m "Release 1.2.1"
git push origin main --tags
```

- [ ] Version tag pushed
- [ ] GitHub release created with changelog notes

## Post-Release

- [ ] GitHub release notes published
- [ ] `README.md` PyPI badge showing correct version
- [ ] Announce in relevant channels if applicable

---

**Reminder:** Each version can only be uploaded to PyPI once. Verify on TestPyPI first.
