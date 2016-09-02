from django.conf.urls import (
    url,
    include)


urlpatterns = [
    url('^learnit/', include('django_learnit.urls', namespace='django_learnit'))
]
