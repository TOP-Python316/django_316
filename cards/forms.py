# cards/forms.py

from django import forms
from .models import Category


class CardForm(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    answer = forms.CharField(
        label='Ответ',
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols": 40}),
        max_length=5000
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Выберите категорию',
        widget=forms.Select(attrs={"class": "form-control"}),
    )
