## Features

* Remove all existing local migration files and recreate them as initial migrations
* Configuration singleton in Django admin to prepare your clean-up deployment
* Management command for your pipeline to update Django's migration history table to reflect the changed migrations

## Motivation

Working with any proper ORM will result in database changes which are reflected in migration files to update your
different environment's database structure. These files are versioned in your repository and if you follow any of the
most popular deployment approaches, they won't be needed when they are deployed on production. This means, they clutter
your repo, might lead to merge conflicts in the future and will slow down your test setup.

Django's default way of handling this is called "squashing". This approach is covered broadly in the
[official documentation](https://docs.djangoproject.com/en/dev/topics/migrations/#migration-squashing). The main
drawback here is, that you have to take care of circular dependencies between models. Depending on your project's
size, this can take a fair amount of time.

The main benefit of squashing migrations is, that the history stays intact, therefore it can be used for example in
package which can be installed by anybody and you don't have control over their database.

If you are working on a "regular" application, you have full control over your data(bases) and once everything has
been applied on the "last" system, typically production, the migrations are obsolete. To avoid spending much time on
fixing squashed migrations you won't need, you can use the "migration zero" pattern. In a nutshell, this means:

* Delete all your local migration files
* Recreate initial migration files containing your current model state
* Fix the migration history on every of your environments
