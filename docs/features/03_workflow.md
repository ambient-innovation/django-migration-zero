# Workflow

Using the migration zero patterns requires a number of steps and prerequisites which have to be executed in a very
specific order to avoid breaking the production database. The following steps will show you how you reset migrations in
a given branch.

## TL;DR

1. Add `manage.py handle_migration_zero_reset` to your migration/post-deploy script
2. Remove and recreate local migration files with `manage.py reset_local_migration_files`
3. Commit local changes to a new branch
4. Go to admin and set flag and timestamp
5. Run deployment
6. Read this page properly before starting any of this! ☝️

## 1. Setup

* Install this package and **DEPLOY IT IN A SEPARATE COMMIT** before you start deleting migrations.
* Add the following command to your script which runs your migrations on deployment and add it BEFORE you
  run `manage.py migrate`

* If you have non-superusers accessing your admin, make sure to only give the
  permission `migration_zero.view_migrationzeroconfiguration` to technical administrators. If you have non-technical
  admin users, consider creating groups instead of the superuser flag to avoid that somebody by accident activates the
  migration zero deployment.

```shell
python ./manage.py handle_migration_zero_reset
```

## 2. Prerequisites

* Ensure that your deployment branches are properly merged into each other. This means, all commits from `master` are
  in `stage`, all commits from `stage` are in `develop`. Your branches might have other names but the important thing is
  that you don't have any commits lying around in upstream branches which are not yet inside the downstream ones.

* Ensure that all migrations in the branch you are working on have been applied in its database

## 3. Local clean-up

Ensure that you have no model changes whatsoever in your application

```shell
python ./manage.py makemigrations
```

* Ensure that all your migrations are applied

```shell
python ./manage.py migrate
```

* Create a new branch called something remotely resembling "refactor/migration-zero-cleanup"

* Now you can run the provided management command to clean up your local migrations. This will track your local files,
  delete them and run `manage.py makemigrations` to create neat and shiny initial migrations per local app

* Add all changes to your branch and commit it

* Create a merge/pull request. **DO NOT merge it yet.**

```shell
python ./manage.py reset_local_migration_files
```

## 4. Preparing the target system

Log into the Django admin, look for the "Migration Zero Configuration" and enable the switch and change the date to
the date of the deployment (probably "today"). **This step is crucial! Don't forget it!** If you don't do this, your
migration reset deployment won't do any database clean-up and your next migration run will fail.

## 5. Deployment

Merge your merge/pull request and deploy to your target system. This will then
execute `manage.py handle_migration_zero_reset` and adjust Django's migration history to reflect the new initial
migrations.

# Updating depending environments

## Case: Merge all your environments upstream in "one go"

If you have a fast deployment cycle, and you can directly merge your develop branch upstream to your stage, demo,
production or what-ever system, the next steps are easy. Just merge your just migration-zero-updated branch upstream.
Since all upstream commits are already in your current branch (see prerequisites), all migrations are already squashed.
Here's what you have to do:

### 1. Merge the downstream branch

Imagine, your develop branch has just been updated, now you want to reset your `stage` migrations. Then you
merge `develop` into `stage` locally and create a merge/pull request. **DO NOT merge it yet.**

### 2. Preparing the target system

Log into the Django admin, look for the "Migration Zero Configuration" and enable the switch and change the date to
the date of the deployment (probably "today"). **This step is crucial! Don't forget it!** Otherwise, you can't "prepare"
the migration reset release in the Django admin and your next migration run will crash.

### 3. Deployment

Merge your merge/pull request and deploy to your target system. This will then execute
`manage.py handle_migration_zero_reset` and adjust Django's migration history to reflect the new initial migrations.

## Case: Starting upstream and merging changes downstream

Some projects are in a state where you can just merge all your deployment branches upstream. Usually, this reflects in a
slow deployment cycle which is a thing you want to avoid. Nevertheless, if you have this situation, it might be even
more pressing to clean up your migrations from time to time to avoid fixing migration mismatches due to hotfixes and
cherry-picking.

Here's what you have to do:

### 1. Prepare the most upstream branch

* Usually, production is the most upstream system. Follow the instructions from the beginning of this page.

### 2. Check for data migrations

Django can only create structural migrations. This would contain adding, renaming or deleting a table or field. Data
migrations are custom code you'll execute
with [RunPython](https://docs.djangoproject.com/en/4.2/ref/migration-operations/#django.db.migrations.operations.RunPython)
to change your data. The provided script won't actively look for data migrations, so you have to manually check for
all migration files which have not yet been applied to all systems and "rescue" them manually. This means in most
cases, you copy the code somewhere, recreate all migrations and then create a new migration file and add your code
again.

### 3. Merge downstream

Merge your branch into the next one downstream. This branch will most likely contain migrations you didn't have yet in
your previous branch. You can use the reset management command with the `--exclude-initials` parameter to just
recreate what's different in your current branch. Afterward, create a merge/pull request and add your changed files.
**DO NOT merge it yet.**

```shell
python ./manage.py reset_local_migration_files --exclude-initials
```

### 4. Preparing the target system

Log into the Django admin, look for the "Migration Zero Configuration" and enable the switch and change the date to
the date of the deployment (probably "today"). **This step is crucial! Don't forget it!**

### 5. Deployment

Merge your merge/pull request and deploy to your target system. This will then execute
`manage.py handle_migration_zero_reset` and adjust Django's migration history to reflect the new initial migrations.

### 6. Repeat these steps downstream until you've reached the last environment

Usually, this means you start at `master`, continue to `stage` and end at `develop`.

## Case: Updating a not-yet-merged branch

Once the migrations are cleaned up in `develop`, all your developers will have to adjust all of their oopen
feature/bugfix/refactoring branches. The pattern is basically the same as *"Starting upstream and merging
changes downstream"*.

### 1. Check for data migrations

Django can only create structural migrations. This would contain adding, renaming or deleting a table or field. Data
migrations are custom code you'll execute
with [RunPython](https://docs.djangoproject.com/en/4.2/ref/migration-operations/#django.db.migrations.operations.RunPython)
to change your data. The provided script won't actively look for data migrations, so you have to manually check for
all migration files which have not yet been applied to all systems and "rescue" them manually. This means in most
cases, you copy the code somewhere, recreate all migrations and then create a new migration file and add your code
again.

### 2. Merge downstream

Merge your branch into the next one downstream. This branch will most likely contain migrations you didn't have yet in
your previous branch. You can use the reset management command with the `--exclude-initials` parameter to just
recreate what's different in your current branch. Afterward, create a merge/pull request and add your changed files.
**DO NOT merge it yet.**

### 3. Fixing your local database

Obviously, you have to update the migration history of your local database as well. The easy way is to just import an
already updated database from - for example - your test system. If you want to keep your database, just navigate to the
local admin interface, enable the migration switch and run the adjustment command.

```shell
python ./manage.py handle_migration_zero_reset
```
