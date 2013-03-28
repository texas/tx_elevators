import json

from django.http import HttpResponse
from django.views.generic import View

from .models import Elevator


class ElevatorList(View):
    def get(self, request, **kwargs):
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
        return self.render_to_response(context)

    def render_to_response(self, context):
        content = json.dumps(context)
        return HttpResponse(content, content_type='application/json')
