from __future__ import division

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "geocode buildings."

    def handle_noargs(self, *args, **options):
        import time
        from django.db.models import Sum
        from tx_elevators.models import Building

        verbosity = int(options['verbosity'])  # default: 1

        qs = Building.objects.filter(latitude__isnull=True).\
            annotate(sum_floors=Sum('elevator__floors')).\
            order_by('-sum_floors')
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
