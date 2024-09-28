import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver

from anki.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
from cards.models import Card
from .telegram_bot import send_telegram_message


@receiver(post_save, sender=Card)
def send_telegram_notification(sender, instance, created, **kwargs):
    if created:
        message = f"""
*Новая карточка!*
*Вопрос:* {instance.question}
*Ответ:* {instance.answer}
*Категория:* {instance.category}
*Теги:* {', '.join(instance.tags.all().values_list('name', flat=True))}
*Автор:* {instance.author}
        """
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))
