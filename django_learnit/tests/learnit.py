from ..library import Library
from ..learning.base import LearningModel

register = Library()


class TestModel(LearningModel):
    name = 'testmodel'

register.learning_model(TestModel)
