from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # поля, которые будут отображаться в админке
    list_display = ('pk', 'question', 'category', 'views', 'upload_date',)
    # поля, которые будут ссылками
    list_display_links = ('pk', 'upload_date',)
    # поля, по которым можно проводить поиск
    search_fields = ('answer',)  # не забываем поставить запятую в конце, если у нас только одно значение, чтобы показать Python, что это кортеж
    # поля, по которым мы можем проводить фильтрацию
    list_filter = ('category',)
    # сортировка по полям
    ordering = ('-views', 'category')
    # изменение выводимого количества элементов на страницу
    list_per_page = 25
    # поля, которые можно редактировать напрямую
    list_editable = ('views', 'question')


# сначала задаётся класс, который добавляет модель в админку
# потом этот класс связывается с админкой через admin.site.register()
# либо сразу через декоратор @admin.register(Card)
# admin.site.register(Card, CardAdmin)