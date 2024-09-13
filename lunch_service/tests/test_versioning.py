import pytest
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from lunch_service.versioning import CustomXAPIHeaderVersioning

pytestmark = pytest.mark.unit


@pytest.fixture
def versioning() -> CustomXAPIHeaderVersioning:
    return CustomXAPIHeaderVersioning()


@pytest.mark.parametrize("version_header, expected_version", [
    ('1.0', '1.0'),
    ('2.0', '2.0'),
])
def test_valid_version_headers(versioning: CustomXAPIHeaderVersioning, version_header: str, expected_version: str) -> None:
    factory: APIRequestFactory = APIRequestFactory()
    request: Request = factory.get('/', HTTP_X_API_VERSION=version_header)
    version: str = versioning.determine_version(request)
    assert version == expected_version


@pytest.mark.parametrize("invalid_version_header", ('3.0', 'unknow-text'))
def test_invalid_version_header(versioning: CustomXAPIHeaderVersioning, invalid_version_header: str) -> None:
    factory: APIRequestFactory = APIRequestFactory()
    request: Request = factory.get('/', HTTP_X_API_VERSION=invalid_version_header)
    with pytest.raises(exceptions.NotAcceptable):
        versioning.determine_version(request)


def test_no_version_header(versioning: CustomXAPIHeaderVersioning) -> None:
    factory: APIRequestFactory = APIRequestFactory()
    request: Request = factory.get('/')
    version: str = versioning.determine_version(request)
    assert version == versioning.default_version
