from django.core.exceptions import ValidationError
from datetime import date

def validate_for_restricted_symbols(value):
    restricted_symbols = '@#$%^&*_+='
    for symbol in restricted_symbols:
        if symbol in value:
            raise ValidationError(f'title must not contain {restricted_symbols}')
    return value

def validate_for_restricted_words(value: str):
    restricted_words = ['skami', 'satvale', 'damteni', 'botli']
    for word in restricted_words:
        if word in value.lower():
            raise ValidationError(f'title must not contain restricted_words')
    return value

def validate_future_date(value: date):
    if value > date.today():
        raise  ValidationError('date must not be from future')
    return value