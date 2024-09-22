from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cards.models import Card


class Command(BaseCommand):

    help = 'Создание группы Moderators и назначение права change_card'

    def handle(self, *args, **kwargs):
        # Создаем или получаем группу "Moderators"
        moderators_group, created = Group.objects.get_or_create(name='Moderators')
        # Получаем контентный тип для модели Card
        content_type = ContentType.objects.get_for_model(Card)
        # Получаем разрешение change_card
        change_card_permission = Permission.objects.get(codename='change_card', content_type=content_type)
        # Добавляем разрешение группе "Moderators"
        moderators_group.permissions.add(change_card_permission)
        
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Moderators' создана и права назначены!"))
        else:
            self.stdout.write(self.style.SUCCESS("Группа 'Moderators' уже существует и права обновлены!"))