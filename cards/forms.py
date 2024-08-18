# cards/forms.py

from django import forms
from .models import Category
from django.core.exceptions import ValidationError
import re


class CodeBlockValidator:
    def __call__(self, value):
        # Проверяем, содержит ли текст маркер начала блока кода
        if '```' not in value:
            return

        # Ищем все блоки кода, заключённые в ```
        code_blocks = re.findall(r'```[\s\S]+?```', value)

        if not code_blocks:
            raise ValidationError('Нет закрывающей пары ```')

        # проверяем каждый блок кода на соответствие списку правил
        for block in code_blocks:
            self.validate_code_block(block)


    def validate_code_block(self, block):

        # Находим индексы открывающих и закрывающих ```
        opening_tick_index = block.find('```')
        closing_tick_index = block.rfind('```')

        # Если индексы совпадают, значит закрывающие ``` отсутствуют
        if opening_tick_index == closing_tick_index:
            raise ValidationError("Нет закрывающей пары ```.")

        # Проверяем, есть ли пробел перед открывающими ```
        if block[opening_tick_index - 1] == ' ':
            raise ValidationError("Уберите пробел перед открывающими ```.")

        # Определяем начало содержимого после ```
        content_start = opening_tick_index + 3

        # Проверяем, есть ли пробел сразу после открывающих ```
        if block[content_start] == ' ':
            raise ValidationError("Уберите пробел после открывающих ```.")

        # Ищем конец строки с названием языка программирования (первый перенос строки после ```)
        language_name_end = block.find('\n', content_start)
        # Проверяем, есть ли название языка и достаточно ли оно длинное
        if language_name_end == -1 or language_name_end - content_start < 2:
            raise ValidationError("Добавьте название языка программирования после открывающих ```.")

        # Проверяем, есть ли перенос строки после названия языка
        if block[language_name_end + 1] != '\n':
            raise ValidationError(
                "Проверьте, что нет пробелов перед открытием блока кода, и есть перенос строки после названия языка.")

        # Проверяем, нет ли пробелов перед закрывающими ```
        if block[closing_tick_index - 1] == ' ':
            raise ValidationError("Уберите пробел перед закрывающими ```.")


class CardForm(forms.Form):
    question = forms.CharField(
        label='Вопрос',
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    answer = forms.CharField(
        label='Ответ',
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols": 40}),
        max_length=5000,
        validators=[CodeBlockValidator()]
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию',
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={'required': 'Это поле обязательно для заполнения'},
    )
