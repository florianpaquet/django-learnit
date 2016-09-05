from django.conf.urls import url

from .views.detail import LearningModelDetailView
from .views.dispatch import labelleling_view_dispatch


urlpatterns = [
    # # Model main view
    url(
        r'(?P<name>[^/]+)$',
        LearningModelDetailView.as_view(),
        name='learning-model-detail'),

    # Model labelling view
    url(
        r'(?P<name>[^/]+)/(?P<pk>\d+)/$',
        labelleling_view_dispatch,
        name='document-labelling')
]
