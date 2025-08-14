from rest_framework.serializers import ValidationError
import re

def validate_youtube_url(value):
    if not value:
        return
    pattern = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
    )
    if not pattern.match(value):
        raise ValidationError('Допускаются только ссылки на youtube.com или youtu.be')
