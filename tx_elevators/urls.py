from django.conf.urls import patterns, include, url
from django.views.decorators.gzip import gzip_page


from . import chart_views, views


urlpatterns = patterns('',
    url(r'^$', views.Landing.as_view(),
        name="home"),
    url(r'^building/(?P<elbi>\d+)/$', views.BuildingView.as_view(),
        name="building_detail")
)


# chart url patterns
chartpatterns = patterns('',
    url(r'^elevatorlist/$', chart_views.ElevatorList.as_view()),
    url(r'^elevatorlist/data/$', gzip_page(chart_views.ElevatorList.as_view()),
        {'data': True}),
)

urlpatterns += patterns('',
    url(r'^chart/', include(chartpatterns)),
)
