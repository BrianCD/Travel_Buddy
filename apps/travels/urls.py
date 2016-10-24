from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index),
url(r'destination/(?P<trip_id>\d+)$', views.display_trip),
url(r'destination/(?P<trip_id>\d+)/join', views.join_trip),
url(r'add', views.add_trip),
url(r'new', views.new_trip)
]
