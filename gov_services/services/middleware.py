"""
Custom Middleware للأمان
"""
import logging

logger = logging.getLogger('services')


class SecurityHeadersMiddleware:
    """
    إضافة Security Headers لجميع الاستجابات
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self';"
        )
        
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer-Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=()'
        )
        
        return response


class RequestLoggingMiddleware:
    """
    تسجيل جميع الطلبات المشبوهة
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.suspicious_paths = [
            '/admin',
            '.php',
            '.asp',
            '.aspx',
            'wp-admin',
            'phpmyadmin',
            'sql',
            '../',
            '..\\',
        ]

    def __call__(self, request):
        # التحقق من الطلبات المشبوهة
        path = request.path.lower()
        for suspicious in self.suspicious_paths:
            if suspicious in path:
                logger.warning(
                    f'Suspicious request detected: {request.path} from IP: {self.get_client_ip(request)}'
                )
                break
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """الحصول على IP الحقيقي"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlockSuspiciousIPMiddleware:
    """
    حظر عناوين IP المشبوهة
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # قائمة عناوين IP المحظورة (يمكن ربطها بقاعدة البيانات لاحقاً)
        self.blocked_ips = set()

    def __call__(self, request):
        ip = self.get_client_ip(request)
        
        if ip in self.blocked_ips:
            logger.error(f'Blocked IP attempt: {ip}')
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Access Denied')
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """الحصول على IP الحقيقي"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
