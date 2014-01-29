from django.conf.urls import patterns, include, url
from django.views.decorators.gzip import gzip_page


from . import chart_views, views


urlpatterns = patterns('',
    url(r'^$', views.Landing.as_view(),
        name="home"),
    url(r'^building/$', gzip_page(views.BuildingsList.as_view()),
        name="building_list"),
    url(r'^building/(?P<elbi>\d+)-(?P<slug>[-\w]+)/$',
        views.BuildingView.as_view(),
        name="building_detail"),
    url(r'^about/$', views.About.as_view(),
        name='about'),

    # chart url patterns
    url(r'^chart/', include(patterns('',
        url(r'^elevatorlist/(?P<data>data.json)?$',
                gzip_page(chart_views.ElevatorList.as_view()),
                name='elevatorlist'),
        url(r'^locator/(?P<data>data.json)?$',
                gzip_page(chart_views.Locator.as_view()),
                name='locator'),
        url(r'^search/(?P<data>data.json)?$',
                gzip_page(chart_views.Search.as_view()),
                name='search'),
    ), namespace='chart')),
)
