from django import forms


class ClassifierChoicesMixin(object):

    def __init__(self, classes, *args, **kwargs):
        super(ClassifierChoicesMixin, self).__init__(*args, **kwargs)
        self.fields['label'].choices = classes


class SingleLabelClassifierForm(ClassifierChoicesMixin, forms.Form):
    label = forms.ChoiceField(widget=forms.RadioSelect())


class MultiLabelClassifierForm(ClassifierChoicesMixin, forms.Form):
    label = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
