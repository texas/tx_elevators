from __future__ import division
from __future__ import unicode_literals

import csv
import logging

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = 'csv file'
    help = 'dump geo data'

    def handle(self, path, *args, **options):
        from tx_elevators.models import Building

        logger = logging.getLogger(__name__)

        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                elbi, latitude, longitude = row
                building = Building.objects.filter(elbi=elbi).update(
                    latitude=latitude,
                    longitude=longitude,
                )
                logger.debug('elbi: {:>5} updated: {}'.format(elbi, building))
