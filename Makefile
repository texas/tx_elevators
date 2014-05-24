PROJECT=./example_project
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
#
#   -s    don't capture stdout
#
	python $(PROJECT)/manage.py test -s


resetdb:
	python $(PROJECT)/manage.py reset_db --router=default --noinput
	python $(PROJECT)/manage.py syncdb --noinput


scrape:
	cd data && $(MAKE) $(MFLAGS) clean elevator_data_file.csv
	python tx_elevators/scripts/scrape.py data/elevator_data_file.csv


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
	LOGGING=WARN DEBUG=0 python $(PROJECT)/manage.py sync_s3 --dir site --gzip

serve:
	cd site && python -m SimpleHTTPServer 8088


.PHONY: help test resetdb scrape pushdb site upload serve
