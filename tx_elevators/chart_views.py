import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Building, Elevator


class BaseChart(TemplateView):
    """Render a chart and supply its data."""
    def get(self, request, **kwargs):
        if 'data' in kwargs:
            data = self.get_data(request, **kwargs)
            content = json.dumps(data)
            return HttpResponse(content, content_type='application/json')
        else:
            return super(BaseChart, self).get(request, **kwargs)


class ElevatorList(BaseChart):
    template_name = "tx_elevators/charts/elevatorlist.html"

    def get_data(self, request, **kwargs):
        queryset = Elevator.objects.filter(
            floors__gt=0,
            year_installed__gte=1913,
            year_installed__lte=2013,
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
    template_name = "TODO"  # TODO

    def annotate(self, qs):
        for obj in qs:
            yield {
                'elbi': obj.elbi,
                'name_1': obj.name_1,
                'address_1': obj.address_1,
                'city': obj.city,
                'latitude': obj.latitude,
                'longitude': obj.longitude,
            }

    def get_data(self, request, **kwargs):
        queryset = Building.objects.exclude(latitude=None)
        context = list(self.annotate(queryset))
        return context


class Search(BaseChart):
    template_name = "TODO"  # TODO

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
