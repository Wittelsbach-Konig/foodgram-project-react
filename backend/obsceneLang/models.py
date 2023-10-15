from django.db import models
from django.conf import settings


class ForbiddenWord(models.Model):
    """Модель для хранения запрещённых слов.

    Params:
        word (str): Запрещённое слово
    """

    word = models.CharField('Запрещенное слово',
                            max_length=settings.WORD_MAX_LENGTH,
                            unique=True)

    class Meta:
        verbose_name = 'Запрещенное слово'
        verbose_name_plural = 'Запрещенные слова'

    def __str__(self) -> str:
        return self.word
