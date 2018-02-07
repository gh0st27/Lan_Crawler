from django.conf.urls import url
from . import views

urlpatterns = [
    # \lan
    url(r'^$', views.index, name='index'),
    # search_result
    url(r'^(?P<Name>[\w]+)$', views.search_result, name='search_result'),
]
