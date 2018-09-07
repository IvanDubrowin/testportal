from django import forms
from .models import Question


class QuestionChoices(forms.Form):
    choice =((1, ''), (2, ''), (3, ''), (4, ''))
    field = forms.ChoiceField(widget=forms.RadioSelect(), label='', choices=choice)
