from django.apps import AppConfig

from .library import (
    get_installed_libraries,
    get_registered_learning_models)


class LearnItConfig(AppConfig):
    name = 'django_learnit'

    def __init__(self, *args, **kwargs):
        """
        Initialize an empty learning models reference
        """
        super(LearnItConfig, self).__init__(*args, **kwargs)
        self.learning_models = {}

    def ready(self):
        """
        Autodiscover `learnit` modules when django app is ready
        and register learning models libraries
        """
        libraries = get_installed_libraries()
        self.learning_models = get_registered_learning_models(libraries)
