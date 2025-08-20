import base64
import binascii

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import get_authorization_header

from apps.payments.paylov.credentials import get_credentials


def authentication(request) -> bool:
    """
    Authenticate the Paylov request.

    This function authenticates the Paylov request using Basic Authentication.
    Args:
        request (Request): The HTTP request object.
    Returns:
        bool: True if the request is authenticated, False otherwise.
    """

    print("Request: ", request.META)
    auth = get_authorization_header(request).split()

    print("Auth Header: ", auth)

    if not auth or auth[0].lower() != b"basic":
        return False

    if len(auth) != 2:
        return False

    try:
        auth_parts = (
            base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(":")
        )
    except (TypeError, UnicodeDecodeError, binascii.Error):
        return False

    username, password = auth_parts[0], auth_parts[2]
    print("Username password: ", username, password)
    credentials = get_credentials()

    paylov_username = credentials["PAYLOV_USERNAME"]
    paylov_password = credentials["PAYLOV_PASSWORD"]

    return username == paylov_username and password == paylov_password
