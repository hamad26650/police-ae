#!/usr/bin/env python
"""
اختبار حقيقي لإرسال الإيميل - يحاكي ما يحصل في Dashboard
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
import django
django.setup()

from django.conf import settings
from services.models import Inquiry
from services.utils.email_service import email_service
import logging

print("="*80)
print("🧪 اختبار حقيقي لإرسال الإيميل")
print("="*80)

# 1. فحص الإعدادات
print("\n📋 1️⃣ فحص إعدادات Gmail:")
print("-"*80)
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '❌ فارغ'}")
print(f"EMAIL_HOST_PASSWORD: {'✅ موجود (' + str(len(settings.EMAIL_HOST_PASSWORD)) + ' حرف)' if settings.EMAIL_HOST_PASSWORD else '❌ فارغ'}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
    print("\n" + "="*80)
    print("❌ الإعدادات غير موجودة!")
    print("="*80)
    print("\n💡 الحل:")
    print("   1. روح DigitalOcean → Settings → Environment Variables")
    print("   2. أضف:")
    print("      EMAIL_HOST_USER = بريدك@gmail.com")
    print("      EMAIL_HOST_PASSWORD = App Password (16 حرف)")
    print("   3. Scope = RUN_AND_BUILD_TIME")
    print("   4. احفظ → Restart → انتظر 3 دقائق")
    print("="*80)
    sys.exit(1)

print("\n✅ الإعدادات موجودة!")

# 2. فحص الاستعلامات
print("\n📋 2️⃣ فحص الاستعلامات:")
print("-"*80)

inquiries = Inquiry.objects.filter(inquiry_type='report_status').order_by('-created_at')[:10]

if not inquiries.exists():
    print("❌ لا توجد استعلامات في قاعدة البيانات!")
    print("   قدم استعلام جديد من الموقع أولاً.")
    sys.exit(1)

print(f"✅ عدد الاستعلامات: {inquiries.count()}")
print("\n📋 آخر 10 استعلامات:")
print("-"*80)

valid_inquiries = []
for i, inq in enumerate(inquiries, 1):
    recipient = inq.email if inq.email else inq.phone
    is_valid = recipient and '@' in recipient
    
    status_icon = "✅" if is_valid else "❌"
    print(f"\n{i}. ID: {inq.id} {status_icon}")
    print(f"   رقم البلاغ: {inq.report_number}/{inq.report_year}")
    print(f"   الإيميل: {recipient}")
    print(f"   صحيح: {'نعم' if is_valid else 'لا - مو إيميل!'}")
    print(f"   الحالة: {inq.get_status_display()}")
    print(f"   تم الرد: {'نعم' if inq.is_resolved else 'لا'}")
    
    if is_valid:
        valid_inquiries.append(inq)

# 3. اختبار الإرسال
if not valid_inquiries:
    print("\n" + "="*80)
    print("❌ جميع الاستعلامات تحتوي على أرقام هواتف بدلاً من إيميلات!")
    print("="*80)
    print("\n💡 الحل:")
    print("   1. قدم استعلام جديد من الموقع")
    print("   2. تأكد من إدخال إيميل صحيح (مثل: test@example.com)")
    print("   3. مو رقم هاتف!")
    print("="*80)
    sys.exit(1)

print("\n" + "="*80)
print(f"✅ عدد الاستعلامات الصحيحة: {len(valid_inquiries)}")
print("="*80)

# اختيار أول استعلام صحيح
test_inquiry = valid_inquiries[0]
recipient = test_inquiry.email if test_inquiry.email else test_inquiry.phone

print(f"\n🧪 3️⃣ اختبار الإرسال للاستعلام #{test_inquiry.id}:")
print("-"*80)
print(f"رقم البلاغ: {test_inquiry.report_number}/{test_inquiry.report_year}")
print(f"الإيميل المستهدف: {recipient}")
print(f"نص الرد التجريبي: هذا رد تجريبي للتأكد من عمل النظام")

print("\n⏳ جاري الإرسال...")

try:
    result = email_service.send_inquiry_response(
        test_inquiry,
        "هذا رد تجريبي للتأكد من عمل النظام.\n\nإذا وصلك هذا الإيميل، معناها النظام يعمل 100%!"
    )
    
    print("\n" + "="*80)
    if result['success']:
        print("✅ نجح الإرسال!")
        print("="*80)
        print(f"\n✉️  تم إرسال إيميل إلى: {recipient}")
        print(f"📨 الرسالة: {result['message']}")
        print("\n💡 تحقق من صندوق الوارد (أو Spam) للإيميل:")
        print(f"   {recipient}")
        print("\n✅ إذا وصل الإيميل، معناها النظام يعمل!")
        print("   جرّب الآن الرد من Dashboard وراح يوصل للمتعامل!")
    else:
        print("❌ فشل الإرسال!")
        print("="*80)
        print(f"\n⚠️  السبب: {result['message']}")
        print("\n💡 الأسباب المحتملة:")
        print("   1. Gmail App Password غير صحيح")
        print("   2. 2-Step Verification مو مفعّل")
        print("   3. الحساب محظور مؤقتاً من Google")
        print("\n🔧 الحل:")
        print("   1. روح: https://myaccount.google.com/apppasswords")
        print("   2. سوّي App Password جديد")
        print("   3. انسخ الـ 16 حرف (بدون spaces)")
        print("   4. حدّث EMAIL_HOST_PASSWORD في DigitalOcean")
        print("   5. Restart التطبيق")
        
except Exception as e:
    print("\n" + "="*80)
    print("❌ حدث خطأ!")
    print("="*80)
    print(f"\n⚠️  نوع الخطأ: {type(e).__name__}")
    print(f"⚠️  التفاصيل: {str(e)}")
    
    error_str = str(e).lower()
    if 'authentication' in error_str or '535' in error_str:
        print("\n💡 المشكلة: خطأ في المصادقة!")
        print("   • App Password غير صحيح")
        print("   • تأكد من نسخ الـ 16 حرف بدون spaces")
    elif 'timeout' in error_str:
        print("\n💡 المشكلة: انتهت المهلة!")
        print("   • مشكلة في الاتصال بـ Gmail")
        print("   • حاول مرة ثانية")
    elif 'connection' in error_str:
        print("\n💡 المشكلة: مشكلة في الاتصال!")
        print("   • تحقق من اتصال الإنترنت")
        print("   • Gmail SMTP ممكن محظور")

print("\n" + "="*80)
print("🎬 انتهى الاختبار")
print("="*80)

