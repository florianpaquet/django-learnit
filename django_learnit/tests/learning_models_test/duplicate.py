from ...library import Library
from ...learning.base import LearningModel

from ..models import Document

register = Library()


# Duplicate
class TestModel(LearningModel):
    name = 'testmodel'
    queryset = Document.objects.all()

register.learning_model(TestModel)
