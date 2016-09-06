from django import forms

from .classifier import ClassifierChoicesMixin


class NamedEntityRecognizerForm(ClassifierChoicesMixin, forms.Form):
    label = forms.ChoiceField(widget=forms.Select())
