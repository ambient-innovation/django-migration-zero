# Common issues & solutions

Here's a list of things that might occur once in a while.

## I deleted a (data) migration I still need

Hopefully, you didn't deploy it yet. If not, just go to your git history and get it back. If not, you have to fix it
manually in your database. Just see what the migration does and follow those steps manually.

## I had to make a hotfix on master containing a migration

As always, if you do hotfixes, make sure to merge them downstream ASAP. The quicker you do it, the less hassle you'll
have in the future.

## I deployed a regular commit with the admin flag active

If you deploy to your environment and by accident have the admin switch active, you shouldn't encounter issues. The
migration history table will have a bunch of updated timestamps but apart from that, you should be fine.

## I deployed a migration zero commit with the admin flag not being active

If you pushed your migration zero commit with all those removed and changed migration files without having the flag
active, you'll encounter a crash when running `manage.py migrate`. Since the migration history is out-of-sync with the
files you just deployed, the migration shouldn't do anything except failing, and you should be OK in 95% of all cases.
Just activate the flag and redeploy.
