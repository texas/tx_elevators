from django.conf.urls import patterns, include, url
from django.views.decorators.gzip import gzip_page


from . import api_views, views


urlpatterns = patterns('',
    url(r'^$', views.Landing.as_view(),
        name="home"),
    url(r'^building/(?P<elbi>\d+)/$', views.BuildingView.as_view(),
        name="building_detail")
)


# api url patterns
apipatterns = patterns('',
    url(r'^elevators/$', gzip_page(api_views.ElevatorList.as_view()))
)

urlpatterns += patterns('',
    url(r'^api/v1/', include(apipatterns)),
)
