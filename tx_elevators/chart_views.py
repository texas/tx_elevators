from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, Sum
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Building, Elevator


class BaseChart(TemplateView):
    """Render a chart and supply its data."""
    template_name = 'tx_elevators/blank.html'

    def get(self, request, **kwargs):
        if kwargs.get('data'):
            data = self.get_data(request, **kwargs)
            encoder = DjangoJSONEncoder()
            content = encoder.encode(data)
            return HttpResponse(content, content_type='application/json')
        else:
            return super(BaseChart, self).get(request, **kwargs)


class ElevatorList(BaseChart):
    template_name = "tx_elevators/charts/elevatorlist.html"

    def get_data(self, request, **kwargs):
        queryset = Elevator.objects.filter(
            floors__gt=0,
            year_installed__gte=1913,
            year_installed__lte=2015,
        ).select_related('building')
        queryset = queryset.exclude(equipment_type__in=[
            'ESCALATOR',
            'MOVING SIDEWALK',
            'WHEELCHAIR LIFT',
            'STAIR CLIMBER',
            'LIMITED USE LIMITED ACCESS',
            'OTHER',
            'UNKNOWN',
        ])
        context = list(queryset.values(
            'floors',
            'equipment_type',
            'year_installed',
            'building__city',
            'building__name_1',
        ))
        return context


class Locator(BaseChart):
    def annotate(self, qs):
        for obj in qs:
            yield {
                'url': obj.get_absolute_url(),
                'name_1': '{0.name_1} ({0.max_floors})'.format(obj),
                'address_1': obj.address_1,
                'city': obj.city,
                'latitude': obj.latitude,
                'longitude': obj.longitude,
            }

    def get_data(self, request, **kwargs):
        queryset = (Building.objects.exclude(latitude=None)
            .annotate(
                sum_floors=Sum('elevator__floors'),
                max_floors=Max('elevator__floors'),
            )
            .filter(sum_floors__gt=0)
        )
        context = list(self.annotate(queryset))
        return context


class Search(BaseChart):
    def get_data(self, request, **kwargs):
        queryset = Building.objects.all()
        context = list(queryset.values(
            'elbi',
            'name_1',
            'address_1',
            'city',
            'zip_code',
        ))
        return context
