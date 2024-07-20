from django.contrib import admin
from .models import Card


admin.site.register(Card)


class CardAdmin(admin.ModelAdmin):
    pass
