from django.core.exceptions import ValidationError
from django.conf import settings

from .utils import is_forbidden, get_forbidden_words


def validate_no_obscenities(value):
    """Кастомный валидатор наличие обсценной/запрещённой лексики."""

    forbidden_words = get_forbidden_words()
    if is_forbidden(value.lower(), forbidden_words, settings.THRESHOLD):
        raise ValidationError(
            "Использование запрещенных слов не допустимо. "
            "Ну и ну вы разочаровали партию. "
            "-10000 социального рейтинга."
        )
    return value
