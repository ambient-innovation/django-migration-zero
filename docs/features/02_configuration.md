# Configuration

# Settings

This package requires all local Django apps to be inside a `BASE_DIR` directory. This directory should be already
defined in the main django settings.

Note that this variable has to be of type `pathlib.Path`.

## Logging

The scripts are quite chatty. If you want to see what's going on under the hood, just configure a quite default-looking
logger in your Django settings.

Note, that in this example, we are only logging to the console.

```python
LOGGING = {
    "loggers": {
        "django_migration_zero": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
```
