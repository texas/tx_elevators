import json

from django.conf import settings
from django.db.models import Count, Max
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView

from .models import Building, Elevator


class Landing(TemplateView):
    template_name = "tx_elevators/landing.html"

    def get_context_data(self, **kwargs):
        context = super(Landing, self).get_context_data(**kwargs)
        tallest_buildings = Building.objects.exclude(
            elevator__floors__isnull=True).annotate(
            height=Max('elevator__floors')).order_by('-height')
        context['tallest_buildings'] = tallest_buildings[:15]
        oldest_elevators = (Elevator.objects
            .exclude(year_installed__lt=1000)
            .select_related('building')
            .order_by('year_installed')
            .distinct('building', 'year_installed')
        )
        context['oldest_elevators'] = oldest_elevators[:15]
        densest_buildings = Building.objects.exclude(
            elevator__floors__isnull=True).annotate(
            num_elevators=Count('elevator')).order_by('-num_elevators')
        context['densest_buildings'] = densest_buildings[:15]
        return context


class BuildingView(DetailView):
    model = Building
    slug_field = 'elbi'
    slug_url_kwarg = 'elbi'

    def post(self, request, **kwargs):
        # for debugging
        if not settings.DEBUG:
            return HttpResponse(status_code=403)
        instance = self.get_object()
        lat = request.POST.get('coords[latitude]')
        lng = request.POST.get('coords[longitude]')
        instance.latitude = lat
        instance.longitude = lng
        instance.save()
        content = json.dumps({
            'status': 'OK',
        })
        return HttpResponse(content, content_type='application/json')


class BuildingsList(ListView):
    queryset = Building.objects.all().order_by('name_1')


class About(TemplateView):
    template_name = 'tx_elevators/about.html'

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        # in order of appearance
        elevators = Elevator.objects.all()
        buildings = Building.objects.all()
        context['elevators'] = elevators
        context['buildings'] = buildings
        context['passenger_elevators'] = elevators.filter(
            equipment_type='PASSENGER')
        context['freight_elevators'] = elevators.filter(
            equipment_type='FREIGHT')
        context['moving_sidewalks'] = elevators.filter(
            equipment_type='MOVING SIDEWALK')
        context['escalators'] = elevators.filter(equipment_type='ESCALATOR')
        context['future'] = elevators.filter(year_installed__gt=2016).\
            select_related('building').order_by('year_installed')
        context['past'] = elevators.filter(year_installed__lt=1000).\
            select_related('building').order_by('year_installed')
        context['geocoded'] = buildings.filter(latitude__isnull=False)
        return context
