# Zerobyte SDK — Project Summary

## Overview

`py-zerobyte` is a Python SDK that wraps the Zerobyte REST API. It provides a clean, typed interface for managing backup volumes, repositories, snapshots, schedules, and notifications. The sole runtime dependency is `requests`.

## Package Structure

```
py-zerobyte/
├── py_zerobyte/
│   ├── __init__.py           # Public surface: ZerobyteClient + exceptions
│   ├── client.py             # ZerobyteClient, _make_request, session management
│   ├── exceptions.py         # ZerobyteError hierarchy
│   ├── auth.py               # better-auth endpoints (sign-in, sign-out, etc.)
│   ├── volumes.py            # /api/v1/volumes — CRUD, mount, files
│   ├── repositories.py       # /api/v1/repositories — CRUD, doctor, rclone
│   ├── snapshots.py          # /api/v1/repositories/{name}/snapshots — list, restore
│   ├── backup_schedules.py   # /api/v1/backups — flat schedule API
│   ├── notifications.py      # /api/v1/notifications/destinations — CRUD, test
│   └── system.py             # /api/v1/system — info, restic password
├── examples/
│   ├── basic_usage.py
│   ├── create_backup_setup.py
│   ├── restore_snapshot.py
│   ├── manage_notifications.py
│   └── monitor_status.py
├── tests/
│   └── test_client.py
├── setup.py
├── pyproject.toml
├── requirements.txt
├── swagger.json              # Zerobyte API specification
└── README.md
```

## API Coverage

All 50 endpoints from `swagger.json` are implemented:

| Module | Methods | Endpoints |
|---|---|---|
| `auth` | 6 | `register`, `login`, `logout`, `get_me`, `get_status`, `change_password` |
| `volumes` | 11 | `list`, `create`, `test_connection`, `get`, `update`, `delete`, `mount`, `unmount`, `health_check`, `list_files`, `browse_filesystem` |
| `repositories` | 7 | `list`, `create`, `get`, `update`, `delete`, `doctor`, `list_rclone_remotes` |
| `snapshots` | 5 | `list`, `get_details`, `delete`, `list_files`, `restore` |
| `backup_schedules` | 15 | `list`, `create`, `get`, `update`, `delete`, `get_for_volume`, `run_now`, `stop_backup`, `run_forget`, `get_notifications`, `update_notifications`, `get_mirrors`, `update_mirrors`, `get_mirror_compatibility`, `reorder` |
| `notifications` | 6 | `list_destinations`, `create_destination`, `get_destination`, `update_destination`, `delete_destination`, `test_destination` |
| `system` | 2 | `get_info`, `download_restic_password` |

## Architecture

### ZerobyteClient

Single entry point. `__init__` creates a `requests.Session` and instantiates one API class per domain, stored as attributes (`client.auth`, `client.volumes`, etc.).

All HTTP logic lives exclusively in `_make_request(method, endpoint, data, params, **kwargs)`:
- Builds the URL from `base_url + endpoint`
- Sends JSON body when `data` is provided
- Maps HTTP 400/401/404/5xx to typed exceptions
- Returns parsed JSON (or raw text for non-JSON responses)

### Authentication

The server uses [better-auth](https://www.better-auth.com/). Login posts to `/api/auth/sign-in/username`; the resulting session cookie (`zerobyte.session_token`) is stored in the `requests.Session` and sent automatically on every subsequent request.

`logout()` and `change_password()` require an `Origin` header for CSRF protection. `_get_trusted_origin()` derives `http://localhost:{port}` from the configured base URL, which the server accepts as a trusted origin.

### Resource Identifiers

Most resources use a **shortId** string (e.g. `"0-b-U31s"`) in URL path segments. Numeric `id` fields exist in responses but are not used as path parameters. Always pass `shortId` to get/update/delete/action methods.

Backup schedules are the exception — `get_for_volume()` still accepts a numeric `volume_id`.

### Exception Hierarchy

```
ZerobyteError               ← base; wraps network / SDK errors
├── AuthenticationError     ← 401
└── APIError                ← all other HTTP errors (has .status_code, .response)
    ├── NotFoundError       ← 404
    └── ValidationError     ← 400
```

## Key Design Decisions

1. **Single `_make_request` method** — all HTTP logic in one place; API modules are thin wrappers
2. **Session-based auth** — `requests.Session` handles cookie persistence automatically
3. **String shortIds** — all path parameters are strings; never assume a numeric id
4. **Flat backup API** — `/api/v1/backups/{scheduleId}` with `repositoryId`/`volumeId` as body fields
5. **No runtime deps beyond `requests`** — keeps installation footprint minimal

## Version

Current: **1.2.1** (setup.py, pyproject.toml, py_zerobyte/__init__.py — all three must stay in sync)

## Dependencies

**Runtime:** `requests >= 2.25.0`

**Development:** `pytest`, `pytest-cov`, `black`, `flake8`

## License

MIT — see [LICENSE](LICENSE)
