#!/usr/bin/env python
"""
اختبار إرسال الإيميل - تشخيص المشكلة
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print("="*70)
print("🧪 اختبار نظام الإيميل")
print("="*70)

# 1. التحقق من الإعدادات
print("\n📋 الإعدادات:")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '❌ غير موجود'}")
print(f"   EMAIL_HOST_PASSWORD: {'✅ موجود' if settings.EMAIL_HOST_PASSWORD else '❌ غير موجود'}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# 2. التحقق من إمكانية الإرسال
if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
    print("\n❌ خطأ: يجب إضافة EMAIL_HOST_USER و EMAIL_HOST_PASSWORD!")
    print("\n📝 الخطوات:")
    print("   1. افتح: https://myaccount.google.com/apppasswords")
    print("   2. أنشئ App Password جديد")
    print("   3. في DigitalOcean → Apps → Settings → Environment Variables")
    print("   4. أضف:")
    print("      • EMAIL_HOST_USER = your-email@gmail.com")
    print("      • EMAIL_HOST_PASSWORD = [App Password]")
    print("   5. Save → انتظر redeploy")
    print("\n⚠️ بدون هذه الإعدادات، الإيميلات لن تُرسل!")
else:
    print("\n✅ الإعدادات موجودة!")
    
    # 3. محاولة إرسال إيميل تجريبي
    print("\n📧 محاولة إرسال إيميل تجريبي...")
    
    try:
        send_mail(
            subject='🧪 اختبار من نظام شرطة الشارقة',
            message='هذا إيميل تجريبي للتأكد من عمل النظام.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # إرسال للنفس
            fail_silently=False,
        )
        print("✅ تم إرسال الإيميل التجريبي بنجاح!")
        print(f"   تحقق من بريدك: {settings.EMAIL_HOST_USER}")
    except Exception as e:
        print(f"❌ فشل الإرسال: {e}")
        print("\n💡 الأسباب المحتملة:")
        print("   • App Password غير صحيح")
        print("   • Gmail 2-Step Verification غير مفعّل")
        print("   • الحساب محظور مؤقتاً")

print("\n" + "="*70)
print("✅ انتهى الاختبار")
print("="*70)
