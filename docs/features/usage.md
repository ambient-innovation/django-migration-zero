# Usage

Using the migration zero patterns requires a number of steps and prerequisites which have to be executed in a very
specific order to avoid breaking the production database.

## Setup

* Install this package and DEPLOY IT IN A SEPARATE COMMIT before you start deleting migrations.
* Add the following command to your script which runs your migrations on deployment and add it BEFORE you run `manage.py migrate`

```shell
python ./manage.py handle_migration_zero_reset
```

## Prerequisites


* Ensure that you have no model changes whatsoever in your application

```shell
python ./manage.py makemigrations
```

* Ensure that all your migrations are applied

```shell
python ./manage.py migrate
```

* Ensure that all migrations in the branch you are working on have been applied in its database

## Local clean-up

* Now you can run the provided management command to clean up your local migrations. This will track your local files,
  delete them and run `manage.py makemigrations` to create neat and shiny initial migrations per local app

```shell
python ./manage.py reset_local_migration_files
```

* Log into the Django admin, look for the "Migration Zero Configuration" and enable the switch and change the date to
  the date of the deployment (probably "today")

* Commit your changes and deploy to your target system
