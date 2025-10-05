"""
Decorators للأمان والحماية
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
import logging

logger = logging.getLogger('services')


def rate_limit(key_prefix, limit=5, period=300):
    """
    Rate limiting decorator
    
    Args:
        key_prefix: prefix للمفتاح في cache
        limit: عدد المحاولات المسموح بها
        period: الفترة الزمنية بالثواني (افتراضياً 5 دقائق)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # الحصول على IP الخاص بالمستخدم
            ip = get_client_ip(request)
            cache_key = f'{key_prefix}:{ip}'
            
            # التحقق من عدد المحاولات
            attempts = cache.get(cache_key, 0)
            
            if attempts >= limit:
                logger.warning(f'Rate limit exceeded for IP: {ip} on {key_prefix}')
                
                # إرجاع استجابة مناسبة حسب نوع الطلب
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'تم تجاوز الحد المسموح. يرجى المحاولة بعد {period // 60} دقائق.'
                    }, status=429)
                else:
                    messages.error(request, f'تم تجاوز الحد المسموح من المحاولات. يرجى المحاولة بعد {period // 60} دقائق.')
                    return render(request, 'services/rate_limit_exceeded.html', status=429)
            
            # تنفيذ الدالة
            response = func(request, *args, **kwargs)
            
            # زيادة العداد فقط إذا كان الطلب POST
            if request.method == 'POST':
                cache.set(cache_key, attempts + 1, period)
            
            return response
        return wrapper
    return decorator


def track_failed_login(max_attempts=5, lockout_time=900):
    """
    تتبع محاولات تسجيل الدخول الفاشلة وقفل الحساب
    
    Args:
        max_attempts: عدد المحاولات الفاشلة المسموحة
        lockout_time: مدة القفل بالثواني (افتراضياً 15 دقيقة)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                username = request.POST.get('username', '').lower()
                ip = get_client_ip(request)
                
                # مفتاح للحساب
                account_key = f'failed_login_account:{username}'
                # مفتاح لـ IP
                ip_key = f'failed_login_ip:{ip}'
                
                # التحقق من القفل
                if cache.get(f'locked:{username}') or cache.get(f'locked_ip:{ip}'):
                    logger.warning(f'Login attempt on locked account/IP: {username}/{ip}')
                    messages.error(request, f'تم قفل الحساب مؤقتاً. يرجى المحاولة بعد {lockout_time // 60} دقيقة.')
                    return render(request, 'services/staff_login.html')
                
                # تنفيذ الدالة
                response = func(request, *args, **kwargs)
                
                # التحقق من نجاح تسجيل الدخول
                if request.user.is_authenticated:
                    # مسح العدادات عند النجاح
                    cache.delete(account_key)
                    cache.delete(ip_key)
                    logger.info(f'Successful login: {username} from {ip}')
                else:
                    # زيادة عداد المحاولات الفاشلة
                    account_attempts = cache.get(account_key, 0) + 1
                    ip_attempts = cache.get(ip_key, 0) + 1
                    
                    cache.set(account_key, account_attempts, lockout_time)
                    cache.set(ip_key, ip_attempts, lockout_time)
                    
                    logger.warning(f'Failed login attempt {account_attempts}/{max_attempts}: {username} from {ip}')
                    
                    # قفل الحساب/IP إذا تجاوز الحد
                    if account_attempts >= max_attempts:
                        cache.set(f'locked:{username}', True, lockout_time)
                        logger.error(f'Account locked: {username}')
                        messages.error(request, f'تم قفل الحساب بعد {max_attempts} محاولات فاشلة. يرجى المحاولة بعد {lockout_time // 60} دقيقة.')
                    elif ip_attempts >= max_attempts * 2:
                        cache.set(f'locked_ip:{ip}', True, lockout_time)
                        logger.error(f'IP locked: {ip}')
                        messages.error(request, f'تم قفل عنوان IP مؤقتاً.')
                    else:
                        remaining = max_attempts - account_attempts
                        messages.error(request, f'بيانات تسجيل الدخول غير صحيحة. المحاولات المتبقية: {remaining}')
                
                return response
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_client_ip(request):
    """الحصول على IP الحقيقي للمستخدم"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_user_activity(activity_type):
    """
    تسجيل نشاط المستخدم (Audit Trail)
    
    Args:
        activity_type: نوع النشاط
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # تنفيذ الدالة
            response = func(request, *args, **kwargs)
            
            # تسجيل النشاط
            if request.user.is_authenticated:
                ip = get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
                
                logger.info(
                    f'Activity: {activity_type} | '
                    f'User: {request.user.username} | '
                    f'IP: {ip} | '
                    f'UserAgent: {user_agent}'
                )
            
            return response
        return wrapper
    return decorator


def require_secure_connection(func):
    """التحقق من الاتصال الآمن (HTTPS) - للإنتاج فقط"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.is_secure() and not request.META.get('HTTP_X_FORWARDED_PROTO') == 'https':
            # في وضع التطوير، نسمح بـ HTTP
            from django.conf import settings
            if not settings.DEBUG:
                return HttpResponse('يجب استخدام اتصال آمن (HTTPS)', status=426)
        
        return func(request, *args, **kwargs)
    return wrapper
