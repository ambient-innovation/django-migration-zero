# Configuration

This package requires all local Django apps to be inside a single directory. This directory needs to be defined in the
main django settings.

Usually, you can use the `BASE_DIR` variable from Django's default setup and add a path.

Note that this variable has to be of type `pathlib.Path`.

```python
MIGRATION_ZERO_APPS_DIR = BASE_DIR / "apps"
```
