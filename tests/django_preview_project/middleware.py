class AnonymousSampleUser:
    is_authenticated = False
    is_anonymous = True


class AuthenticatedSampleUser:
    is_authenticated = True
    is_anonymous = False
    username = "real-session-user"


class SampleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.sample_middleware_marker = "request-middleware-active"
        if request.session.get("preview_authenticated"):
            request.user = AuthenticatedSampleUser()
        else:
            request.user = AnonymousSampleUser()
        response = self.get_response(request)
        response.headers["X-Sample-Middleware"] = "response-middleware-active"
        return response
