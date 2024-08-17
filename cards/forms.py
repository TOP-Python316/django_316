# cards/forms.py

from django import forms


class CardForm(forms.Form):
    question = forms.CharField(label='Вопрос', max_length=100)
    answer = forms.CharField(label='Ответ', widget=forms.Textarea, max_length=5000)