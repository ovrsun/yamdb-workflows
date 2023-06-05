import re

from django.core.exceptions import ValidationError


def validate_username(name):
    regex = re.compile(r'^[\w.@+-]+')
    if not regex.match(name):
        raise ValidationError(
            'Недопустимые символы в имени!'
        )
    if name == 'me':
        raise ValidationError(
            'Такое имя недоступно!'
        )
    if name is None or name == '':
        raise ValidationError(
            'Нужно заполнить!'
        )
