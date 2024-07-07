from django import template


# в Django это регистрация библиотеки шаблонов, которая позволяет использовать пользовательские теги
# и фильтры в шаблонах Django.

register = template.Library()

# @register это декоратор, который используется в Django для создания простых пользовательских тегов шаблонов.
# simple_tag - это декоратор, который используется для создания простых пользовательских тегов шаблонов.
@register.simple_tag
def markdown_to_html(markdown_text: str) -> str:
    return markdown_text.upper() # просто для теста