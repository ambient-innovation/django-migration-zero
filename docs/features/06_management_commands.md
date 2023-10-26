# Management Commands

## reset_local_migration_files

This command will delete every migration file within your local Django apps and afterward call `makemigrations` to
recreate new and shiny initial migrations.

It comes with a couple of parameters:

| Option             | Explanation                                                                                                                                                                                         |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --dry-run          | Won't delete any files. Useful to check if your setup is correct.                                                                                                                                   |
| --exclude-initials | Won't replace and recreate initial migration files. Useful when you are merging a clean "migration zero" commit into your branch and just want to replace the migration delta to the source branch. |

## handle_migration_zero_reset

This command will prepare and adjust Django's migration history table in the database to reflect the newly created
initial migrations. It needs the migration zero configuration switch in your database to be active, otherwise it won't
do anything.

In a nutshell, it will remove all previous history records in the database and add one new record for every migration
file coming in the "migration zero" commit.
