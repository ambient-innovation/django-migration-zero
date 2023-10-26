# Architecture

This page will describe the process and the decisions taken by the creators of this package.

## Resetting local files

* The command for resetting your local migration files will iterate your Django app directory and looks for packages
  containing migration.
* Then it detects all migration files, optionally leaving out the initials.
* In the next step, every detected file will be deleted. You can run the process as a dry run, which won't delete the
  files.
* Finally, the command calls Django's "makemigrations" to recreate the migration files neat and clean.

## Handle database adjustments

* This command will first validate that the migration configuration database singleton (exactly one record in the
  database) exists and is valid
* Afterward, it checks if the flag is active and the migration date is set to "today"
* Then it will fetch the list of local Django apps and delete all records in the history table `django_migrations`
  where `app` equals current app label. Due to working a little around the framework, it's not possible to
  use `migrate [APP] --prune` or `migrate --fake [APP] zero`
* In the next step, we'll populate the migration table with `migrate --fake` which will create a record per detected
  migration file
* To ensure we have a clean state by now, we ask for Django's opinion via `migrate --check`
* If the check passes, we disable the admin flag to avoid staring the process for the next deployment again
