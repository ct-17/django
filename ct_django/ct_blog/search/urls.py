from django.conf.urls import url

from .views import Search

urlpatterns = [
    url(r'^$', Search.as_view(), name='query'),
]

