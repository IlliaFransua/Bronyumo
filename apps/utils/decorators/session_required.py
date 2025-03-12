from functools import wraps
from django.http import HttpResponse
from apps.accounts.managers import CompanySessionManager
from Bronyumo.settings import db_dsn

def session_required(view_func):
    """
    A decorator that ensures the request has a valid session. If the session is valid,
    the wrapped view function is called. If the session is invalid or expired, a 403
    response is returned. The session expiration time is refreshed if the session is valid.

    :param view_func: The view function to be wrapped and protected by the session check.
    :return: A wrapped version of the original view function that requires a valid session.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        """
        The wrapped view function that checks if the session is valid before executing
        the original view. If the session is valid, the session expiration time is refreshed
        and the original view is executed. If the session is invalid or expired, a 403
        response is returned.

        :param request: The HTTP request object containing the session data (from cookies).
        :param args: Additional positional arguments to be passed to the original view function.
        :param kwargs: Additional keyword arguments to be passed to the original view function.
        :return: A response object, either the result of the original view function or a 403 error.
        """
        session_id = request.COOKIES.get('session_id')

        if session_id is None:
            return HttpResponse("Session not found. Please log in.", status=403)

        session_manager = CompanySessionManager(db_dsn=db_dsn)

        if not session_manager.validate_session(session_id):
            return HttpResponse("Session is invalid or expired.", status=403)

        if session_manager.refresh_session(session_id):
            response = view_func(request, *args, **kwargs)
            response.set_cookie('session_id', session_id, max_age=3600)
            return response

        return view_func(request, *args, **kwargs)

    return _wrapped_view
