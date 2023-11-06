# Introduction

## Why do I need this package?

Migrations will pile up in your application over the course of
time. [Squashing](https://docs.djangoproject.com/en/dev/topics/migrations/#migration-squashing) takes time to resolve
all those circular dependencies within your models and in the end, you do work for something that you don't need. All
migrations have been applied, so the structural and data changes are not relevant for you anymore.

The "migration zero" approach will help you get rid of those migration files. But most solutions or packages
will only help you do a local clean-up while the tricky part is to update your migration history on
your deployed systems.

Surely, you can log into your production system and run a series of commands manually but this is always a high-stress
situation. What if something goes sideways? Secondly, not everybody has access to all environments. And lastly, this
task is tedious and takes time. And we all know that you won't implement a habit (like cleaning up your migrations
regularly) when it's annoying and time-consuming.

That's why we've built this package. It helps you clean up all those files AND will handle all the things that need to
happen on your databases, no matter where they live and how you can access them.

## Requirements

* All local Django apps are inside one directory
* You are in full control of every database your application runs on
    * This wouldn't be the case if you are creating a python package.
      Use [squashing](https://docs.djangoproject.com/en/dev/topics/migrations/#migration-squashing) in that case.
* You're using some kind of CI/CD pipeline for an automated deployment
* You have dedicated branches for every environment you deploy to
    * e.g. `master` deploys to your production system, `develop` deploys to your test system
* All migrations in every deployment branch have been applied to their database
* Having access to the Django admin of every environment you want to reset the migrations on

## Literature

* [“Migrations zero” or how to handle migrations on a large Django project, X. Dubuc, 2018](https://medium.com/@xavier.dubuc/migrations-zero-or-how-to-handle-migrations-on-a-large-django-project-643627938449)
* [How to Reset Migrations, V. Freitas, 2016](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)

## Alternatives

### [django-zeromigrations](https://pypi.org/project/django-zeromigrations/)

Implements the local cleanup quite verbosely, including a backup functionality. Lacks the CI/CD part, though.
