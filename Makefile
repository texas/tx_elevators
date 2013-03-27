PROJECT=./example_project

help:
	@echo "make commands:"
	@echo "  make help    - this help"
	@echo "  make test    - run test suite"
	@echo "  make resetdb - drop and recreate the database"


test:
#
#   -s    don't capture stdout
#
	python $(PROJECT)/manage.py test -s


resetdb:
	python $(PROJECT)/manage.py reset_db --router=default --noinput
	python $(PROJECT)/manage.py syncdb --noinput


scrape:
	cd data && $(MAKE) $(MFLAGS)
	python tx_elevators/scrapers.py data/elevator_data_file.csv


.PHONY: help test resetdb scrape
