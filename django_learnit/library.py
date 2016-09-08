from importlib import import_module

from django.apps import apps

from .exceptions import (
    InvalidLearningModel,
    DuplicateLearningModelName)
from .learning.base import LearningModel


class Library(object):

    def __init__(self):
        """
        Initialize an empty learning models library
        """
        self.learning_models = {}

    def learning_model(self, model_class):
        """
        Registers a `model_class` sublassing `LearningModel` in the library.

        Adding a model whose name is already registered raises a
        `DuplicateLearningModelName` exception
        """
        # Check subclass
        if not issubclass(model_class, LearningModel):
            raise InvalidLearningModel(
                "%(cls)s model does not inherit from `LearningModel`." % {
                    'cls': model_class.__name__
                })

        # Check model name is unique
        model_name = model_class.get_name()

        if model_name in self.learning_models:
            raise DuplicateLearningModelName(
                "%(cls)s uses '%(name)s' that is already exists in the model library" % {
                    'cls': model_class.__name__,
                    'name': model_name
                })

        # Add model to the library
        self.learning_models[model_name] = model_class()


def import_library(name):
    """
    Imports and returns the register attribute in library module
    """
    module = import_module(name)
    return module.register


def get_installed_libraries():
    """
    Returns registered libraries in any `learning_models` module
    at the root of all installed applications
    """
    libraries = []

    candidates = [
        '%s.learning_models' % app_config.name
        for app_config in apps.get_app_configs()
    ]

    for candidate in candidates:
        try:
            module = import_module(candidate)
        except ImportError:
            continue

        if hasattr(module, 'register'):
            libraries.append(candidate)

    return libraries


def get_registered_learning_models(libraries):
    """
    Returns a dict with registered learning models as (model_name: model_obj)
    """
    learning_models = {}

    for library in libraries:
        register = import_library(library)

        for model_name, model_obj in register.learning_models.items():
            # Check model name is unique
            if model_name in learning_models:
                raise DuplicateLearningModelName(
                    "%(cls)s uses '%(name)s' that is already exists in the model library" % {
                        'cls': model_obj.__class__.__name__,
                        'name': model_name
                    })

            learning_models[model_name] = model_obj

    return learning_models


def get_learning_model(learning_model_name):
    """
    Returns the registered learning model or None
    """
    app_config = apps.get_app_config('django_learnit')
    learning_models = app_config.learning_models

    if learning_model_name in learning_models:
        return learning_models[learning_model_name]

    return None
