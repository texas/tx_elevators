from django.conf.urls import patterns, include, url
from django.views.decorators.gzip import gzip_page


from . import chart_views, views


urlpatterns = patterns('',
    url(r'^$', views.Landing.as_view(),
        name="home"),
    url(r'^building/$', gzip_page(views.BuildingsList.as_view()),
        name="building_list"),
    url(r'^building/(?P<elbi>\d+)/$', views.BuildingView.as_view(),
        name="building_detail")
)


# chart url patterns
chartpatterns = patterns('',
    url(r'^elevatorlist/$', chart_views.ElevatorList.as_view()),
    url(r'^elevatorlist/data.json$', gzip_page(chart_views.ElevatorList.as_view()),
        {'data': True}),
    url(r'^locator/data.json$', gzip_page(chart_views.Locator.as_view()),
        {'data': True}),
    url(r'^search/data.json$', gzip_page(chart_views.Search.as_view()),
        {'data': True}),
)

urlpatterns += patterns('',
    url(r'^chart/', include(chartpatterns)),
)
