from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.versioning import BaseVersioning


class CustomXAPIHeaderVersioning(BaseVersioning):
    """
    GET /something/ HTTP/1.1
    Host: example.com
    X-API-VERSION: 1.0
    """
    VERSION_HEADER_NAME = 'X-API-VERSION'

    def __init__(self) -> None:
        super().__init__()
        self.invalid_version_message = _(f'Invalid version in "{self.VERSION_HEADER_NAME}" header.')

    def determine_version(self, request, *args, **kwargs):
        version = request.headers.get(self.VERSION_HEADER_NAME, self.default_version)
        if not self.is_allowed_version(version):
            raise exceptions.NotAcceptable(self.invalid_version_message)
        return version
