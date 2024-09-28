import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver

from anki.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
from cards.models import Card
from .telegram_bot import send_telegram_message


@receiver(post_save, sender=Card)
def send_telegram_notification(sender, instance, created, **kwargs):
    message_template = f"""
*Вопрос:* {instance.question}
*Ответ:* {instance.answer}
*Категория:* {instance.category}
*Автор:* {instance.author}
"""
    if created:
        message = '*Новая карточка!*\n' + message_template
    else:
        message = f'*Карточка* {instance.id} изменена:\n' + message_template

    asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))
