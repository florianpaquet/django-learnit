from django.test import TestCase

from ..exceptions import (
    InvalidLearningModel,
    DuplicateLearningModelName)
from ..learning.base import LearningModel
from ..library import (
    Library,
    get_installed_libraries,
    import_library,
    get_registered_learning_models,
    get_learning_model)

from .learning_models import TestModel


class LibraryTestCase(TestCase):

    def setUp(self):
        self.register = Library()

    def test_register_raises_when_not_a_learning_model(self):
        """Raise excpetion when registering something that is not a learning model"""
        class TestModel(object):
            pass

        with self.assertRaises(InvalidLearningModel):
            self.register.learning_model(TestModel)

    def test_register_raises_when_name_is_duplicate(self):
        """Raise excpetion when registering a duplicate name"""
        class TestModel(LearningModel):
            name = 'testmodel'

        class OtherModel(LearningModel):
            name = 'testmodel'

        self.register.learning_model(TestModel)

        with self.assertRaises(DuplicateLearningModelName):
            self.register.learning_model(OtherModel)

    def test_register_models(self):
        """Registers the learning models"""
        class TestModel(LearningModel):
            name = 'testmodel'

        class OtherModel(LearningModel):
            name = 'othermodel'

        self.register.learning_model(TestModel)
        self.register.learning_model(OtherModel)

        self.assertEqual(len(self.register.learning_models), 2)
        self.assertEqual(self.register.learning_models['testmodel'].__class__, TestModel)
        self.assertEqual(self.register.learning_models['othermodel'].__class__, OtherModel)

    def test_installed_libraries(self):
        """Returns installed libraries"""
        installed_libraries = get_installed_libraries()
        self.assertIn('django_learnit.tests.learning_models', installed_libraries)

    def test_import_library(self):
        """Returns libraby in module"""
        from .learning_models import register as original_register

        register = import_library('django_learnit.tests.learning_models')
        self.assertEqual(register, original_register)

    def test_registered_learning_models(self):
        """Returns the learning models dict"""
        libraries = get_installed_libraries()
        learning_models = get_registered_learning_models(libraries)
        self.assertEqual(len(learning_models), 4)
        self.assertEqual(learning_models['testmodel'].__class__, TestModel)

    def test_get_non_existing_learning_model(self):
        """Returns None when model is not registered"""
        self.assertIsNone(get_learning_model('notregistered'))

    def test_get_learning_model(self):
        """Returns the registered model class"""
        self.assertEqual(get_learning_model('testmodel').__class__, TestModel)

    def test_register_on_different_module_raises_on_duplicate(self):
        """Raise exception when registering duplicate name in different modules"""
        libraries = get_installed_libraries()
        libraries.append('django_learnit.tests.learning_models_test.duplicate')

        with self.assertRaises(DuplicateLearningModelName):
            get_registered_learning_models(libraries)
