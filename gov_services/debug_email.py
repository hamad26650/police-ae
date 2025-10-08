#!/usr/bin/env python
"""
تشخيص مشكلة الإيميل - فحص شامل
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from services.models import Inquiry
from services.utils.email_service import email_service

print("="*70)
print("🔍 تشخيص مشكلة الإيميل")
print("="*70)

# 1. فحص الإعدادات
print("\n📋 1. فحص إعدادات SMTP:")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '❌ غير موجود'}")
print(f"   EMAIL_HOST_PASSWORD: {'✅ موجود (' + str(len(settings.EMAIL_HOST_PASSWORD)) + ' حرف)' if settings.EMAIL_HOST_PASSWORD else '❌ غير موجود'}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
    print("\n❌ خطأ: الإعدادات غير موجودة!")
    print("   تأكد من إضافتها في DigitalOcean Environment Variables")
    exit(1)

print("\n✅ الإعدادات موجودة!")

# 2. اختبار اتصال SMTP
print("\n📧 2. اختبار إرسال إيميل تجريبي:")
try:
    send_mail(
        subject='🧪 اختبار - نظام شرطة الشارقة',
        message='هذا اختبار للتأكد من عمل SMTP',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print("✅ نجح إرسال الإيميل التجريبي!")
    print(f"   تحقق من بريدك: {settings.EMAIL_HOST_USER}")
except Exception as e:
    print(f"❌ فشل إرسال الإيميل التجريبي:")
    print(f"   الخطأ: {type(e).__name__}: {str(e)}")
    print("\n💡 الأسباب المحتملة:")
    print("   • Gmail App Password غير صحيح")
    print("   • 2-Step Verification غير مفعّل")
    print("   • الحساب محظور مؤقتاً")
    print("   • تأكد من نسخ الـ 16 حرف بدون spaces")
    exit(1)

# 3. فحص الاستعلامات
print("\n📋 3. فحص الاستعلامات في قاعدة البيانات:")
inquiries = Inquiry.objects.filter(inquiry_type='report_status').order_by('-created_at')[:5]

if not inquiries.exists():
    print("⚠️ لا توجد استعلامات في قاعدة البيانات")
    print("   قدم استعلام جديد من الموقع أولاً")
else:
    print(f"✅ عدد الاستعلامات: {inquiries.count()}")
    print("\n📋 آخر 5 استعلامات:")
    for inq in inquiries:
        print(f"\n   ID: {inq.id}")
        print(f"   رقم البلاغ: {inq.report_number}/{inq.report_year}")
        print(f"   البريد (email field): {inq.email or '❌ فارغ'}")
        print(f"   البريد (phone field): {inq.phone or '❌ فارغ'}")
        
        # تحديد الإيميل الفعلي
        recipient = inq.email if inq.email else inq.phone
        
        if recipient and '@' in recipient:
            print(f"   ✅ الإيميل الفعلي: {recipient}")
        else:
            print(f"   ❌ الإيميل غير صحيح: {recipient}")
            print(f"      المشكلة: المتعامل أدخل رقم هاتف بدلاً من إيميل!")
        
        print(f"   الحالة: {inq.get_status_display()}")
        print(f"   تم الرد: {'✅ نعم' if inq.is_resolved else '❌ لا'}")
        if inq.is_resolved:
            print(f"   الرد: {inq.response[:50]}...")

# 4. اختبار email_service
print("\n📧 4. اختبار email_service:")
if inquiries.exists():
    test_inquiry = inquiries.first()
    print(f"   جاري اختبار الإرسال للاستعلام #{test_inquiry.id}...")
    
    # التحقق من الإيميل
    recipient = test_inquiry.email if test_inquiry.email else test_inquiry.phone
    
    if not recipient or '@' not in recipient:
        print(f"   ❌ لا يمكن الاختبار - الإيميل غير صحيح: {recipient}")
        print("   💡 قدم استعلام جديد مع إيميل صحيح")
    else:
        try:
            result = email_service.send_inquiry_response(
                test_inquiry,
                "هذا رد تجريبي للتأكد من عمل النظام"
            )
            
            if result['success']:
                print(f"   ✅ نجح الإرسال!")
                print(f"   الإيميل: {recipient}")
                print(f"   الرسالة: {result['message']}")
            else:
                print(f"   ❌ فشل الإرسال:")
                print(f"   الرسالة: {result['message']}")
        except Exception as e:
            print(f"   ❌ خطأ: {type(e).__name__}: {str(e)}")

print("\n" + "="*70)
print("✅ انتهى التشخيص")
print("="*70)

# 5. ملخص النتائج
print("\n📊 الملخص:")
print("="*70)

if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    print("✅ إعدادات Gmail موجودة")
else:
    print("❌ إعدادات Gmail غير موجودة")

if inquiries.exists():
    valid_emails = sum(1 for inq in inquiries if (inq.email or inq.phone) and '@' in (inq.email or inq.phone or ''))
    print(f"✅ الاستعلامات: {inquiries.count()}")
    print(f"   - إيميلات صحيحة: {valid_emails}")
    print(f"   - إيميلات غير صحيحة: {inquiries.count() - valid_emails}")
else:
    print("⚠️ لا توجد استعلامات")

print("\n💡 التوصيات:")
if not inquiries.exists():
    print("   1. قدم استعلام جديد من الموقع")
    print("   2. تأكد من إدخال إيميل صحيح (مو رقم هاتف!)")
elif valid_emails == 0:
    print("   ❌ جميع الاستعلامات تحتوي على أرقام هواتف بدلاً من إيميلات!")
    print("   1. عدّل نموذج الاستعلام لإجبار إدخال إيميل صحيح")
    print("   2. أو قدم استعلام جديد مع إيميل صحيح")
else:
    print("   ✅ كل شي تمام!")
    print("   جرّب الآن الرد على استعلام من Dashboard")

print("="*70)

