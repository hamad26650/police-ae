"""
إعداد البريد الإلكتروني للتجربة الحقيقية
"""
import os

print("=" * 60)
print("إعداد البريد الإلكتروني للتجربة الحقيقية")
print("=" * 60)
print()

# إعدادات Gmail
print("📧 إعدادات Gmail:")
print()
email_user = input("أدخل إيميل Gmail الخاص بك: ").strip()
print()
print("⚠️  تحتاج إلى App Password من Gmail")
print("   اذهب إلى: https://myaccount.google.com/apppasswords")
print("   وانسخ كلمة المرور (16 حرف)")
print()
email_password = input("أدخل App Password: ").strip()
print()

# إعدادات إيميلات البنوك
print("🏦 إعدادات إيميلات البنوك:")
print("   (يمكنك استخدام إيميلك الشخصي للاختبار)")
print()

bank_emails = {}
banks = [
    ('بنك ابوظبي التجاري', 'adcb'),
    ('مصرف ابوظبي الاسلامي', 'adib'),
    ('بنك دبي الاسلامي', 'dib'),
]

for bank_name, bank_code in banks:
    default_email = f"{email_user.split('@')[0]}+{bank_code}@{email_user.split('@')[1]}"
    print(f"   {bank_name}:")
    bank_email = input(f"      الإيميل (اضغط Enter للاستخدام: {default_email}): ").strip()
    if not bank_email:
        bank_email = default_email
    bank_emails[bank_name] = bank_email
    print()

# حفظ الإعدادات
print("💾 حفظ الإعدادات...")
print()

# إنشاء ملف .env أو تحديث settings.py
env_content = f"""# إعدادات البريد الإلكتروني
EMAIL_HOST_USER={email_user}
EMAIL_HOST_PASSWORD={email_password}
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ تم حفظ إعدادات البريد الإلكتروني في ملف .env")
print()

# تحديث إيميلات البنوك في email_service.py
print("📝 تحديث إيميلات البنوك...")

# قراءة الملف
with open('services/utils/email_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تحديث قاموس الإيميلات
old_dict = """        BANK_EMAILS = {
            'بنك ابوظبي التجاري': 'adcb@bank.ae',  # يمكن تغيير الإيميلات حسب الحاجة
            'مصرف ابوظبي الاسلامي': 'adib@bank.ae',
            'بنك دبي الاسلامي': 'dib@bank.ae',
        }"""

new_dict = f"""        BANK_EMAILS = {{
            'بنك ابوظبي التجاري': '{bank_emails['بنك ابوظبي التجاري']}',
            'مصرف ابوظبي الاسلامي': '{bank_emails['مصرف ابوظبي الاسلامي']}',
            'بنك دبي الاسلامي': '{bank_emails['بنك دبي الاسلامي']}',
        }}"""

content = content.replace(old_dict, new_dict)

# حفظ الملف
with open('services/utils/email_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تحديث إيميلات البنوك")
print()

print("=" * 60)
print("✅ تم الإعداد بنجاح!")
print("=" * 60)
print()
print("الخطوات التالية:")
print("1. تأكد من أن الخادم يعمل: python manage.py runserver")
print("2. افتح: http://127.0.0.1:8000/interior-ministry/bank-contact/")
print("3. املأ النموذج وأرسله")
print("4. تحقق من صندوق الوارد للإيميلات المحددة")
print()


