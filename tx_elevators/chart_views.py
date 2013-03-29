import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Elevator


class ElevatorList(TemplateView):
    template_name = "tx_elevators/charts/elevatorlist.html"

    def get(self, request, **kwargs):
        if 'data' in kwargs:
            return self.get_data(request, **kwargs)
        else:
            return super(ElevatorList, self).get(request, **kwargs)

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
        content = json.dumps(context)
        return HttpResponse(content, content_type='application/json')
