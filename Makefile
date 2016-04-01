PROJECT=./example_project
MANAGE=python $(PROJECT)/manage.py
SITE_URL=localhost:8000

help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"


# TODO actually write some tests
test:
	$(MANAGE) test tx_elevators


resetdb: ## Reset the dev database
	$(MANAGE) reset_db --router=default --noinput
	$(MANAGE) migrate --noinput

# Note that `geocode` will still re-lookup bad addresses
#
# To restore: `django loadgeo data/geocoding.csv`
dumpgeo: ## Dump building geo data
	$(MANAGE) dumpgeo > data/geocoding.csv

scrape: ## Scrape new data
	cd data && $(MAKE) $(MFLAGS) clean elevator_data_file.csv
	python tx_elevators/scripts/scrape.py data/elevator_data_file.csv
	@echo "should geocode the top 1000 too: $(MANAGE) geocode"


# timing for trivial import real	1m51.994s
# timing for a fresh import real	4m15.279s
import:
	python tx_elevators/scripts/scrape.py data/elevator_data_file.csv


# FINISHED --2013-04-01 00:10:54--
# Total wall clock time: 43m 29s
# Downloaded: 24343 files, 92M in 5.3s (17.3 MB/s)
#
# FINISHED --2014-11-01 16:38:55--
# Total wall clock time: 9m 4s
# Downloaded: 25615 files, 120M in 0.8s (150 MB/s)
site:
	bin/download_site.sh

serve:
	cd site && python -m SimpleHTTPServer 8088

# requires installing https://github.com/twpayne/s3-parallel-put
# uses 8 threads by default
#
# INFO:s3-parallel-put[statter-12800]:put 137686194 bytes in 28270 files in 697.4 seconds (197436 bytes/s, 40.5 files/s)
upload:
	cd site && s3-parallel-put --quiet --bucket=${AWS_BUCKET_NAME} \
	  --grant public-read --header "Cache-Control:max-age=2592000" --gzip .
