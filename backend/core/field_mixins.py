import binascii
from base64 import b64decode
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from rest_framework import serializers


class CustomBase64ImageFieldMixin(serializers.ImageField):
    """Кастомное поле для кодирования/декодирования в base64."""

    EMPTY_VALUES = (None, "", [], (), {})

    @property
    def INVALID_TYPE_MESSAGE(self):
        raise NotImplementedError

    def to_representation(self, obj):
        """Преобразование объекта в строку или другой формат для чтения."""
        return obj.image.url

    def to_internal_value(self, data):
        """Метод преобразования картинки."""
        if data in self.EMPTY_VALUES:
            return None
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f'uploaded_image.{ext}'

            try:
                decoded_file = b64decode(imgstr)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)

            data = ContentFile(decoded_file, name=filename)
        return super().to_internal_value(data)
