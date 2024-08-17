# cards/forms.py

from django import forms
from .models import Category


class CardForm(forms.Form):
    question = forms.CharField(label='Вопрос', max_length=100)
    answer = forms.CharField(label='Ответ', widget=forms.Textarea, max_length=5000)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Выберите категорию',
    )
