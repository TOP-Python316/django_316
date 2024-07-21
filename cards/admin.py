from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # list_display = ('id', 'question', 'answer', 'upload_date', 'views', 'adds')
    # list_filter = ('upload_date', 'views')
    # fields = ['question', 'answer', ('views', 'adds')]
    pass


# сначала задаётся класс, который добавляет модель в админку
# потом этот класс связывается с админкой через admin.site.register()
# либо сразу через декоратор @admin.register(Card)
# admin.site.register(Card, CardAdmin)