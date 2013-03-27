from __future__ import division

from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "geocode buildings."

    option_list = BaseCommand.option_list + (
        make_option('-n', '--count',
            dest='count',
            help='Only geocode this many'),
        )

    def handle(self, *args, **options):
        import time
        from django.db.models import Sum
        from tx_elevators.models import Building

        verbosity = int(options['verbosity'])  # default: 1
        count = options['count']
        qs = Building.objects.filter(latitude__isnull=True).\
            annotate(sum_floors=Sum('elevator__floors')).\
            order_by('-sum_floors')
        if count is not None:
            qs = qs[:int(count)]
        count = qs.count()
        for i, building in enumerate(qs):
            if verbosity:
                print "%6d/%d %d-%s" % (i, count, building.pk, building)
            try:
                building.geocode()
                time.sleep(86400 / 2500)  # 2500 geolocation requests/day limit
            except KeyboardInterrupt:
                exit(1)
            except ValueError:
                pass
