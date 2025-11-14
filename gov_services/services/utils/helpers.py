"""
دوال مساعدة مشتركة
Common Helper Functions
"""


def get_client_ip(request):
    """
    الحصول على عنوان IP الحقيقي للمستخدم
    Get real client IP address
    
    Args:
        request: Django request object
        
    Returns:
        str: عنوان IP الحقيقي
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # في حالة وجود proxy، الـ IP الأول هو IP المستخدم الحقيقي
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

