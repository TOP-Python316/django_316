# cards/forms.py

from django import forms
from .models import Category, Card, Tag
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


class TagStringValidator:
    def __call__(self, value):
        if ' ' in value:
            raise ValidationError('Теги не должны содержать пробелов')

class CardForm(forms.ModelForm):

    # в этих блоках можно определять только поля, которые мы хотим кастомизировать
    answer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 40}),
        label='Ответ',
        validators=[CodeBlockValidator()]
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Категория не выбрана',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    tags = forms.CharField(
        label='Теги',
        required=False,
        help_text='Перечислите теги через запятую, без пробелов',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[TagStringValidator()]
    )

    class Meta:
        model = Card  # модель с которой работаем форма
        fields = ['question', 'answer', 'category', 'tags']  # поля, которые будут в форме и их порядок

        # Виджеты для полей
        widgets =  {
            'question': forms.TextInput(attrs={'class': 'form-control'})
        }

        # Метки для полей
        labels = {
            'question': 'Вопрос',
        }

    def clean_tags(self):
        # преобразование строки тегов в список тегов
        tags_str = self.cleaned_data['tags'].lower()
        tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tag_list

    def save(self, *args, **kwargs):
        # Мы получаем экземпляр карточки. Без commit=False карточка сохранится в базу данных
        # При попытке сохранения, необработанные теги приведут к ошибке
        # В этом режиме мы получаем только экземпляр карточки.
        instance = super().save(commit=False)
        # Сохраняем карточку в базу данных, чтобы у нее появился id
        # Без id мы не сможем добавить теги
        instance.save()

        # Новый функционал для редактирования карточки (старые теги и новые теги)
        current_tags = set(self.cleaned_data['tags'])

        # Новый функционал для редактирования карточки (старые теги и новые теги)
        for tag in instance.tags.all():
            if tag.name not in current_tags:
                instance.tags.remove(tag)

        # Добавляем новые теги
        for tag_name in current_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            instance.tags.add(tag)

        return instance


class UploadFileForm(forms.Form):
    # Здесь определяется поле для загрузки файла
    file = forms.FileField(label='Выберите файл', widget=forms.FileInput(attrs={'class': 'form-control'}))