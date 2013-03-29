import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Elevator


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
            floors__gt=0, year_installed__lte=2013).select_related('building')
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
            'decal',
            'floors',
            'equipment_type',
            'year_installed',
            'building__elbi',
            'building__latitude',
            'building__longitude',
        ))
        return context
