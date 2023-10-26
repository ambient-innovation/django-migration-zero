class MissingMigrationZeroConfigRecordError(RuntimeError):
    pass


class InvalidMigrationTreeError(RuntimeError):
    pass


class InvalidMigrationAppsDirPathError(ValueError):
    pass
