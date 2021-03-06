from __future__ import division

from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "geocode buildings."

    option_list = BaseCommand.option_list + (
        make_option('-n', '--count',
            dest='count',
            help='Only geocode this many'),
        make_option('-w', '--wait',
            dest='wait',
            default=86400 / 2500,  # 2500 geolocation requests/day limit
            help='Wait this many seconds (defaults to 35)'),
        )

    def handle(self, *args, **options):
        import logging
        import time

        from django.db.models import Sum
        from tx_elevators.models import Building
        from geopy.geocoders.googlev3 import GeocoderQueryError

        logger = logging.getLogger(__name__)

        verbosity = int(options['verbosity'])  # default: 1
        count = options['count']
        wait = float(options['wait'])
        qs = Building.objects.filter(latitude__isnull=True).\
            annotate(sum_floors=Sum('elevator__floors')).\
            order_by('-sum_floors')
        if count is not None:
            qs = qs[:int(count)]
        count = qs.count()
        for i, building in enumerate(qs, start=1):
            if verbosity:
                print ("{0:6}/{1} {2.elbi}-{2} (pk: {2.pk}) "
                       "(rank: {2.sum_floors})").format(
                    i, count, building)
            try:
                building.geocode()
                time.sleep(wait)
            except KeyboardInterrupt:
                exit(1)
            except (ValueError, TypeError, GeocoderQueryError) as e:
                # ignore bad address ValueError
                # ignore geocode lookup failed TypeError
                # ignore no address GeocoderQueryError
                logger.error('Geocode Lookup Failed: {}'.format(e))
