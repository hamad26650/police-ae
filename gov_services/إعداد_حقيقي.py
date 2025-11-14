"""
إعداد البريد الإلكتروني للتجربة الحقيقية
قم بتشغيل هذا الملف وأدخل معلوماتك
"""
import os
import sys
import django

# إعداد Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from services.models import Center

print("=" * 70)
print("إعداد البريد الإلكتروني للتجربة الحقيقية")
print("=" * 70)
print()

# إعدادات Outlook
print("📧 الخطوة 1: إعدادات Outlook/Microsoft")
print("-" * 70)
print("لإرسال الإيميلات، تحتاج إلى:")
print("1. حساب Outlook/Hotmail/Microsoft 365")
print("2. كلمة المرور (أو App Password إذا كان التحقق الثنائي مفعّل)")
print()
print("ملاحظات مهمة:")
print("   → إذا كان التحقق الثنائي مفعّل، تحتاج App Password")
print("   → اذهب إلى: https://account.microsoft.com/security")
print("   → ثم 'Advanced security options' > 'App passwords'")
print("   → أو استخدم كلمة المرور العادية إذا لم يكن التحقق الثنائي مفعّل")
print()
print("-" * 70)
print()

email_user = input("✉️  أدخل إيميل Outlook/Hotmail الخاص بك: ").strip()
if not email_user:
    print("❌ يجب إدخال الإيميل!")
    sys.exit(1)

email_password = input("🔐 أدخل كلمة المرور (أو App Password): ").strip()
if not email_password:
    print("❌ يجب إدخال كلمة المرور!")
    sys.exit(1)

print()
print("=" * 70)
print("📧 الخطوة 2: إيميلات البنوك للاختبار")
print("=" * 70)
print()
print("يمكنك استخدام إيميلك الشخصي للاختبار، أو إيميلات حقيقية للبنوك")
print("(يمكنك الضغط Enter لاستخدام إيميلك الشخصي للاختبار)")
print()

bank_emails = {}
banks = [
    ('بنك ابوظبي التجاري', 'adcb'),
    ('مصرف ابوظبي الاسلامي', 'adib'),
    ('بنك دبي الاسلامي', 'dib'),
]

for bank_name, bank_code in banks:
    default_email = email_user  # استخدام نفس الإيميل للاختبار
    print(f"🏦 {bank_name}:")
    bank_email = input(f"   الإيميل (Enter للاستخدام: {default_email}): ").strip()
    if not bank_email:
        bank_email = default_email
    bank_emails[bank_name] = bank_email
    print(f"   ✅ سيتم الإرسال إلى: {bank_email}")
    print()

print()
print("=" * 70)
print("🏢 الخطوة 3: إيميلات مراكز الشرطة")
print("=" * 70)
print()

centers = list(Center.objects.all())
center_emails = {}

if not centers:
    print("⚠️ لا يوجد مراكز في قاعدة البيانات حالياً. سيتم تخطي هذه الخطوة.")
else:
    for center in centers:
        default_center_email = center.email or email_user
        print(f"🏛️ {center.name}:")
        center_email = input(f"   الإيميل (Enter للاستخدام: {default_center_email}): ").strip()
        if not center_email:
            center_email = default_center_email
        center.email = center_email
        center.save()
        center_emails[center.name] = center_email
        print(f"   ✅ تم حفظ الإيميل: {center_email}")
        print()

print()
print("=" * 70)
print("💾 حفظ الإعدادات...")
print("=" * 70)
print()

# تحديث email_service.py
print("📝 تحديث إيميلات البنوك في email_service.py...")

try:
    with open('services/utils/email_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن قاموس الإيميلات وتحديثه
    import re
    pattern = r"BANK_EMAILS = \{[^}]+\}"
    
    new_dict = f"""BANK_EMAILS = {{
            'بنك ابوظبي التجاري': '{bank_emails['بنك ابوظبي التجاري']}',
            'مصرف ابوظبي الاسلامي': '{bank_emails['مصرف ابوظبي الاسلامي']}',
            'بنك دبي الاسلامي': '{bank_emails['بنك دبي الاسلامي']}',
        }}"""
    
    content = re.sub(pattern, new_dict, content, flags=re.DOTALL)
    
    with open('services/utils/email_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم تحديث إيميلات البنوك")
    
except Exception as e:
    print(f"❌ خطأ في تحديث الملف: {e}")
    sys.exit(1)

# إنشاء ملف batch لتشغيل الخادم مع الإعدادات
print()
print("📝 إنشاء ملف تشغيل مع الإعدادات...")

batch_content = f"""@echo off
title تشغيل الموقع مع إعدادات البريد الإلكتروني
echo ============================================
echo    تشغيل الموقع مع إعدادات البريد الإلكتروني
echo ============================================
echo.

set EMAIL_HOST_USER={email_user}
set EMAIL_HOST_PASSWORD={email_password}

cd /d "%~dp0"
"..\gov_services_env\Scripts\python.exe" manage.py runserver

pause
"""

with open('start_with_email.bat', 'w', encoding='utf-8') as f:
    f.write(batch_content)

print("✅ تم إنشاء ملف start_with_email.bat")
print()

print("=" * 70)
print("✅ تم الإعداد بنجاح!")
print("=" * 70)
print()
print("الخطوات التالية:")
print()
print("1️⃣  شغل الموقع باستخدام:")
print("   → ملف: start_with_email.bat")
print("   → أو في Terminal:")
print(f"      set EMAIL_HOST_USER={email_user}")
print(f"      set EMAIL_HOST_PASSWORD={email_password}")
print("      python manage.py runserver")
print()
print("2️⃣  افتح المتصفح:")
print("   → http://127.0.0.1:8000/interior-ministry/bank-contact/")
print()
print("3️⃣  املأ النموذج وأرسله")
print()
print("4️⃣  تحقق من صندوق الوارد للإيميلات:")
if center_emails:
    print("   • مراكز الشرطة:")
    for center_name, center_email in center_emails.items():
        print(f"      - {center_name}: {center_email}")
if bank_emails:
    print("   • البنوك:")
    for bank_name, bank_email in bank_emails.items():
        print(f"      - {bank_name}: {bank_email}")
print()
print("=" * 70)

