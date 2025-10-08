#!/usr/bin/env python
"""
فحص تلقائي عند كل Deploy - يتشغل تلقائياً
"""
import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
import django
django.setup()

from django.conf import settings

print("\n" + "="*80)
print("🔍 فحص تلقائي - Email Configuration")
print("="*80)

email_user = os.environ.get('EMAIL_HOST_USER', None)
email_pass = os.environ.get('EMAIL_HOST_PASSWORD', None)

issues = []

# Check environment variables
if not email_user:
    issues.append("❌ EMAIL_HOST_USER غير موجود في Environment Variables")
else:
    print(f"✅ EMAIL_HOST_USER: {email_user}")

if not email_pass:
    issues.append("❌ EMAIL_HOST_PASSWORD غير موجود في Environment Variables")
else:
    print(f"✅ EMAIL_HOST_PASSWORD: موجود (طوله {len(email_pass)} حرف)")

# Check Django settings
if not settings.EMAIL_HOST_USER:
    issues.append("❌ settings.EMAIL_HOST_USER فارغ")
else:
    print(f"✅ Django settings.EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

if not settings.EMAIL_HOST_PASSWORD:
    issues.append("❌ settings.EMAIL_HOST_PASSWORD فارغ")
else:
    print(f"✅ Django settings.EMAIL_HOST_PASSWORD: موجود")

# Results
print("\n" + "-"*80)
if not issues:
    print("✅ كل إعدادات الإيميل صحيحة!")
    print("✅ الإيميلات راح تُرسل للمتعاملين!")
    
    # Try sending test email
    try:
        from django.core.mail import send_mail
        print("\n🧪 اختبار إرسال سريع...")
        send_mail(
            'اختبار تلقائي - Deploy جديد',
            'تم Deploy بنجاح وإعدادات الإيميل تعمل!',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("✅ تم إرسال إيميل تجريبي بنجاح!")
    except Exception as e:
        print(f"⚠️ فشل إرسال إيميل تجريبي: {e}")
        print("   (ممكن يكون App Password غير صحيح)")
else:
    print("⚠️ تحذير: إعدادات الإيميل ناقصة!")
    for issue in issues:
        print(f"   {issue}")
    print("\n💡 يرجى إضافة EMAIL_HOST_USER و EMAIL_HOST_PASSWORD في:")
    print("   DigitalOcean → Settings → Environment Variables")

print("="*80 + "\n")

# Don't fail the deployment even if email settings are missing
sys.exit(0)

