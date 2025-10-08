#!/usr/bin/env python
"""
فحص سريع لإعدادات الإيميل - 30 ثانية
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')

import django
django.setup()

from django.conf import settings

print("="*80)
print("🔍 فحص إعدادات الإيميل - نتيجة سريعة")
print("="*80)

# 1. فحص Environment Variables
print("\n📋 Environment Variables من DigitalOcean:")
print("-"*80)

email_user = os.environ.get('EMAIL_HOST_USER', None)
email_pass = os.environ.get('EMAIL_HOST_PASSWORD', None)

if email_user:
    print(f"✅ EMAIL_HOST_USER موجود: {email_user}")
else:
    print("❌ EMAIL_HOST_USER غير موجود في Environment Variables")

if email_pass:
    print(f"✅ EMAIL_HOST_PASSWORD موجود: (طوله {len(email_pass)} حرف)")
else:
    print("❌ EMAIL_HOST_PASSWORD غير موجود في Environment Variables")

# 2. فحص Django Settings
print("\n📋 Django Settings (ما يقرأه الكود):")
print("-"*80)

if settings.EMAIL_HOST_USER:
    print(f"✅ settings.EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
else:
    print("❌ settings.EMAIL_HOST_USER: فارغ!")

if settings.EMAIL_HOST_PASSWORD:
    print(f"✅ settings.EMAIL_HOST_PASSWORD: (طوله {len(settings.EMAIL_HOST_PASSWORD)} حرف)")
else:
    print("❌ settings.EMAIL_HOST_PASSWORD: فارغ!")

print(f"\nℹ️  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"ℹ️  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"ℹ️  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"ℹ️  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# 3. النتيجة النهائية
print("\n" + "="*80)
if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    print("✅ الإعدادات موجودة - الإيميلات **راح تُرسل**!")
    print("\n💡 إذا ما وصلت الإيميلات:")
    print("   1. تحقق من App Password صحيح (16 حرف بدون spaces)")
    print("   2. تحقق من 2-Step Verification مفعّل في Gmail")
    print("   3. شغّل: python test_email.py للاختبار")
else:
    print("❌ الإعدادات ناقصة - الإيميلات **ما راح تُرسل**!")
    print("\n🔧 الحل:")
    print("   1. روح DigitalOcean → Settings → Environment Variables")
    print("   2. تأكد من إضافة:")
    print("      • EMAIL_HOST_USER = بريدك@gmail.com")
    print("      • EMAIL_HOST_PASSWORD = App Password (16 حرف)")
    print("   3. احفظ واضغط \"Restart\" على التطبيق")
    print("   4. انتظر 2-3 دقائق وشغّل هذا السكريبت مرة ثانية")

print("="*80)

# 4. اختبار إرسال سريع (فقط إذا الإعدادات موجودة)
if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    print("\n🧪 اختبار إرسال سريع...")
    print("-"*80)
    try:
        from django.core.mail import send_mail
        send_mail(
            '✅ اختبار - النظام يعمل!',
            'هذا إيميل تجريبي. إذا وصلك، معناها الإعدادات صحيحة 100%',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("✅ نجح الإرسال! تحقق من بريدك الآن.")
    except Exception as e:
        print(f"❌ فشل الإرسال: {e}")
        print("\n💡 المشكلة على الأرجح:")
        print("   • App Password غير صحيح (تأكد من الـ 16 حرف)")
        print("   • 2-Step Verification مو مفعّل")

