from Levenshtein import distance
from typing import Set

from .models import ForbiddenWord


def get_forbidden_words() -> Set[str]:
    """Получить множество нецензурных слов."""
    forbidden_words = ({w.lower() for w in
                       ForbiddenWord.objects.values_list('word', flat=True)})
    return forbidden_words


def get_words_from_text(text_string: str) -> Set[str]:
    """Получить множество слов из текста."""
    return {w for w in text_string.lower().split()}


def is_forbidden(word: str, forbidden_words: Set[str], threshold: int):
    """Проверка слова с помощью расстояния Левенштейна."""
    for forbidden_word in forbidden_words:
        levenshtein_distance = distance(word, forbidden_word)
        if levenshtein_distance <= threshold:
            return True
    return False


def text_has_forbidden_words(set_string: Set[str],
                             forbidden_words_set: Set[str],
                             threshold: int) -> bool:
    """Проверка текста с помощью расстояния Левенштейна."""
    for word in set_string:
        if is_forbidden(word, forbidden_words_set, threshold):
            return True
    return False
