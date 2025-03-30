from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if isinstance(value, dict):
            value = value.get(self.field, '')

        if not isinstance(value, str) or not bool('youtube.com' in value.lower()):
            raise ValidationError('Некорректная ссылка.')
