from django.conf.urls import url

from .views.base import RandomUnlabelledDocumentRedirectView
from .views.detail import LearningModelDetailView
from .views.list import LearningModelListView
from .views.dispatch import labelleling_view_dispatch


urlpatterns = [
    # Model list view
    url(
        r'^$',
        LearningModelListView.as_view(),
        name='learning-model-list'),

    # Model detail view
    url(
        r'(?P<name>[^/]+)$',
        LearningModelDetailView.as_view(),
        name='learning-model-detail'),

    # Random unlabelled redirect
    url(
        r'(?P<name>[^/]+)/random/$',
        RandomUnlabelledDocumentRedirectView.as_view(),
        name='random-document-labelling'),

    # Model labelling view
    url(
        r'(?P<name>[^/]+)/(?P<pk>\d+)/$',
        labelleling_view_dispatch,
        name='document-labelling')
]
