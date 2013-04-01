============
Tx Elevators
============
Dev Setup
---------

Installing Requirements::

    pip install -r requirements-dev.txt


Using Postgresql instead of Sqlite as your database::

    export DATABASE_URL='postgres:///tx_elevators'


Deploying to Heroku
-------------------

Create a new app and give it a database::

    $ heroku apps:create
    $ heroku addons:add heroku-postgresql:dev

Promote the database to ``DATABASE_URL``::

    $ heroku config | grep HEROKU_POSTGRESQL
    HEROKU_POSTGRESQL_RED_URL: postgres://user3123:passkja83kd8@ec2-117-21-174-214.compute-1.amazonaws.com:6212/db982398
    $ heroku pg:promote RED

Install the pgbackups addon::

    $ heroku addons:add pgbackups

Migrate data from your local Postgresql to Heroku (https://devcenter.heroku.com/articles/heroku-postgres-import-export)::

    $ pg_dump -Fc --no-acl --no-owner tx_elevators > tx_elevators.dump

Upload ``tx_elevators.dump`` someplace on the Internets and pull it into Heroku::

    $ heroku pgbackups:restore DATABASE http://example.com/tx_elevators.dump


Deploying to S3
---------------

Partial instructions for deploying to a `hosted site on S3`_):

1. Make sure you're not in debug mode.
2. Make sure this project is running locally on ``http://localhost:8000``.
3. Run ``make site upload``

.. _hosted site on S3: http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html
