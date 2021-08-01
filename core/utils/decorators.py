from django.conf import settings
from django.http import HttpResponseForbidden
from structlog import get_logger


def api_key_required():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            logger = get_logger(__name__).bind(action='authorization_check')

            key = request.META.get('HTTP_AUTHORIZATION', 'missing_api_key')
            if key != settings.API_KEY:
                logger.error('invalid_api_key')
                return HttpResponseForbidden()

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
