#!/usr/bin/env python
"""
سكريبت بسيط لاختبار إرسال الإيميلات عبر Gmail
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """اختبار إرسال إيميل"""
    print("🔄 جاري اختبار إرسال الإيميل...")
    print(f"📧 من: {settings.EMAIL_HOST_USER}")
    
    try:
        send_mail(
            subject='🧪 اختبار إرسال إيميل - Police Portal',
            message='مبروك! إعدادات Gmail تشتغل بشكل صحيح ✅',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # يرسل لنفس الإيميل
            fail_silently=False,
        )
        print("✅ تم إرسال الإيميل بنجاح!")
        print(f"📬 تحقق من بريدك: {settings.EMAIL_HOST_USER}")
        
    except Exception as e:
        print(f"❌ خطأ في إرسال الإيميل:")
        print(f"   {str(e)}")
        print("\n💡 تأكد من:")
        print("   1. إيميلك صحيح في ملف .env")
        print("   2. App Password صحيح (16 رقم من Google)")
        print("   3. التحقق بخطوتين مفعّل في حساب Google")

if __name__ == '__main__':
    test_email()

