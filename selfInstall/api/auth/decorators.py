from functools import wraps

from flask import request

from selfInstall.api.exceptions import ApiUnauthorized, ApiForbidden
from selfInstall.models.users import User
from LoggingFunctions.apiLogger import apiLogger
apiLogger=apiLogger(__name__)

def tokenRequired(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        tokenPayload = checkAccessToken()
        for name, val in tokenPayload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated


def adminTokenRequired(f):
    """Execute function if request contains valid access token AND user is admin."""

    @wraps(f)
    def decorated(*args, **kwargs):
        tokenPayload = checkAccessToken(admin_only=True)
        if not tokenPayload["admin"]:
            raise ApiForbidden()
        for name, val in tokenPayload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated


def checkAccessToken():

    token = request.headers.get("Authorization")
    apiLogger.logInfo(f"decoded token : {token} ")
    if not token:
        raise ApiUnauthorized(description="Unauthorized")
    result = User.decodeAccessToken(token)
    if result == "Access token expired":
        raise ApiUnauthorized(
            description="""Please Contact DL-NTO-Wireless-Analytics <DL-NTO-Wireless-Analytics@charter.com> if you
            believe this to be incorrect""",
            error="INVALID_TOKEN",
            errorDescription="Access token expired",
        )
    elif result == "Invalid token":
        raise ApiUnauthorized(
            description="""Please Contact DL-NTO-Wireless-Analytics <DL-NTO-Wireless-Analytics@charter.com> if you
            believe this to be incorrect""",
            error="INVALID_TOKEN",
            errorDescription="Invalid token",
        )
    if result is None:
        raise ApiUnauthorized(
            description="""Please Contact DL-NTO-Wireless-Analytics <DL-NTO-Wireless-Analytics@charter.com> if you
            believe this to be incorrect""",
            error="INVALID_TOKEN",
            errorDescription="Invalid token",
        )
    return result
