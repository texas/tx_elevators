PROJECT=./example_project
MANAGE=python $(PROJECT)/manage.py
SITE_URL=localhost:8000

help:
	@echo "make commands:"
	@echo "  make help    - this help"
	@echo "  make test    - run test suite"
	@echo "  make resetdb - drop and recreate the database"
	@echo "  make scrape  - get data and import"
	@echo "  make import  - import data"
	@echo "  make site    - spider $(SITE_URL) and save pages locally"
	@echo "  make upload  - sync spidered pages to S3"
	@echo "  make serve   - serve the spided pages locally (on port 8088)"


test:
	$(MANAGE) test tx_elevators


resetdb:
	$(MANAGE) reset_db --router=default --noinput
	$(MANAGE) syncdb --noinput


# Backup the local database
#
# To restore
#   cat tx_elevators-2014-08-31.dump | \
#   docker run --rm --link postgis:postgis -t crccheck/postgis \
#   pg_restore -U docker -h postgis --dbname elevators
dumpdb:
	docker run --rm --link postgis:postgis -t crccheck/postgis \
	  pg_dump -U docker -h postgis -p 5432 -Fc elevators > tx_elevators-$$(date +"%Y-%m-%d").dump

# Dump building geocodes
#
# Note that `geocode` will still re-lookup bad addresses
#
# To restore: `django loadgeo data/geocoding.csv`
dumpgeo:
	$(MANAGE) dumpgeo > data/geocoding.csv

scrape:
	cd data && $(MAKE) $(MFLAGS) clean elevator_data_file.csv
	python tx_elevators/scripts/scrape.py data/elevator_data_file.csv
	@echo "should geocode the top 1000 too: $(MANAGE) geocode"


import:
	python tx_elevators/scripts/scrape.py data/elevator_data_file.csv


dbpush:
	test $(SCP_DUMP)
	test $(SCP_URL)
	pg_dump -Fc --no-acl --no-owner tx_elevators > tx_elevators.dump
	scp tx_elevators.dump $(SCP_DUMP)
	heroku pgbackups:restore DATABASE $(SCP_URL)
	rm tx_elevators.dump


# FINISHED --2013-04-01 00:10:54--
# Total wall clock time: 43m 29s
# Downloaded: 24343 files, 92M in 5.3s (17.3 MB/s)
#
site:
	bin/download_site.sh

# 24340 files uploaded.
# 3 files skipped.
#
# real	200m23.933s
# user	1m29.810s
# sys	1m51.935s
upload:
	LOGGING=WARN DEBUG=0 $(MANAGE) sync_s3 --dir site --gzip

serve:
	cd site && python -m SimpleHTTPServer 8088


.PHONY: help test resetdb scrape pushdb site upload serve
