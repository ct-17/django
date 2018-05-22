from django.conf.urls import url
from . import views
from .views import IotListView, IotDetailView

urlpatterns = [
    url(r'^$', IotListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', IotDetailView.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/comments/$', views.comments, name="comments"),
    url(r'^post/$', views.post_new, name="post_new"),
]
