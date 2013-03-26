from django.conf.urls import patterns, include, url


from . import views


urlpatterns = patterns('',
    url(r'^$', views.Landing.as_view(),
        name="home"),
    url(r'^building/(?P<elbi>\d+)/$', views.BuildingView.as_view(),
        name="building_detail")
)
