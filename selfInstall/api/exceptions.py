from werkzeug.exceptions import Unauthorized, Forbidden


class ApiUnauthorized(Unauthorized):
    """Raise status code 401 with customizable WWW-Authenticate header."""

    def __init__(
        self,
        description="Unauthorized",
        error=None,
        errorDescription=None
            ):
        self.description = description
        self.GetWwwAuthValue = self.GetWwwAuthValue(
            error, errorDescription
        )
        Unauthorized.__init__(
            self, description=description, response=None, www_authenticate=None
        )

    def get_headers(self, environ):
        return [("Content-Type", "text/html"), ("WWW-Authenticate", self.GetWwwAuthValue)]

    def GetWwwAuthValue(self, error, errorDescription):
        wwwAuthValue = ''
        if error:
            wwwAuthValue = f', error="{error}"'
        if errorDescription:
            wwwAuthValue += f', errorDescription="{errorDescription}"'
        return wwwAuthValue


class ApiForbidden(Forbidden):
    """Raise status code 403 with WWW-Authenticate header."""

    description = "You are not an administrator"

    def get_headers(self, environ):
        return [
            ("Content-Type", "text/html"),
            (
                "WWW-Authenticate",
                'error="insufficient_scope',
                'error_description="You are not an administrator"',
            ),
        ]
