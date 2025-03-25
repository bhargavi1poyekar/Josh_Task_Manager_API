# api_logging.py
import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('api')

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        logger.info(
            f"Request: {request.method} {request.path}",
            extra={'user': request.user.username, 'data': request.GET or request.POST}
        )

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        logger.info(
            f"Response: {response.status_code} ({duration:.2f}s)",
            extra={'data': getattr(response, 'data', None)}
        )
        return response

    def process_exception(self, request, exception):
        logger.error(
            f"Error: {str(exception)}", 
            exc_info=True,
            extra={'path': request.path}
        )