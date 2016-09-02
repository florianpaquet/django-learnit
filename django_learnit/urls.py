from django.conf.urls import url

from .views.dispatch import labelleling_view_dispatch


urlpatterns = [
    url(
        r'(?P<name>[^/]+)/(?P<pk>\d+)/$',
        labelleling_view_dispatch,
        name='document-labelling')
]
