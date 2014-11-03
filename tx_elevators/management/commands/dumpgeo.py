from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'dump geo data'

    def handle(self, *args, **options):
        from tx_elevators.models import Building

        for x in Building.objects.filter(latitude__isnull=False).order_by('elbi'):
            print('{elbi},{latitude},{longitude}'.format(**x.__dict__))
