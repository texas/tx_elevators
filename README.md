TX Elevators
============

Dev Setup
---------

Installing Requirements:

    pip install -r requirements-dev.txt


Using Postgresql instead of Sqlite as your database:

    export DATABASE_URL='postgres:///tx_elevators'


Getting Data
------------

If you don't have a database set up, `DEBUG=1 make resetdb` will create one for
you. Running `make scrape` will download a fresh copy of the CSV and import the
data. Afterwards, you can run `manage.py geocode` to geocode the data.


Deploying to S3
---------------

Partial instructions for deploying to a [hosted site on S3]:

1. Make sure you're not in debug mode.
2. Make sure this project is running locally on `http://localhost:8000`.
3. Run `make site upload`

  [hosted site on S3]: http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html
