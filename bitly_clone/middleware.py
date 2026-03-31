import logging
import uuid
import time

logger = logging.getLogger('bitly_requests')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = uuid.uuid4().hex[:8]
        start_time = time.time()
        
        # Add tag to request object so views can use it if they want
        request.log_tag = request_id
        
        # Process the request
        response = self.get_response(request)
        
        duration = round(time.time() - start_time, 3)
        
        # Get client IP safely
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR', 'Unknown')
        
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        
        log_message = (
            f"[Tag: {request_id}] "
            f"User: {user} | "
            f"Method: {request.method} | "
            f"Path: {request.get_full_path()} | "
            f"IP: {client_ip} | "
            f"Status: {response.status_code} | "
            f"Time: {duration}s"
        )
        
        if response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)
            
        return response
