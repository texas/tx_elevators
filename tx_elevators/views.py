"""Sample Views"""
from django.db.models import Count, Max
from django.views.generic import TemplateView

from .models import Building, Elevator


class Landing(TemplateView):
    template_name = "tx_elevators/landing.html"

    def get_context_data(self, **kwargs):
        context = super(Landing, self).get_context_data(**kwargs)
        tallest_buildings = Building.objects.exclude(
            elevator__floors__isnull=True).annotate(
            height=Max('elevator__floors')).order_by('-height')
        context['tallest_buildings'] = tallest_buildings[:15]
        oldest_elevators = Elevator.objects.exclude(
            year_installed__lt=1000).order_by('year_installed')
        context['oldest_elevators'] = oldest_elevators[:15]
        densest_buildings = Building.objects.exclude(
            elevator__floors__isnull=True).annotate(
            num_elevators=Count('elevator')).order_by('-num_elevators')
        context['densest_buildings'] = densest_buildings[:15]
        return context
