from ..library import Library
from ..learning.base import LearningModel
from ..learning.classifier import ClassifierModel

from .models import Document

register = Library()


class TestModel(LearningModel):
    name = 'testmodel'
    queryset = Document.objects.all()

register.learning_model(TestModel)


class TestSingleLabelClassifierModel(ClassifierModel):
    name = 'test_singlelabel_classifier'
    queryset = Document.objects.all()
    classes = (
        (0, 'No'),
        (1, 'Yes')
    )
    multilabel = False

register.learning_model(TestSingleLabelClassifierModel)


class TestMultiLabelClassifierModel(ClassifierModel):
    name = 'test_multilabel_classifier'
    queryset = Document.objects.all()
    classes = (
        (0, 'No'),
        (1, 'Yes')
    )
    multilabel = True

register.learning_model(TestMultiLabelClassifierModel)
