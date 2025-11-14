"""
ملف اختبار إرسال إيميل مخاطبة البنوك
"""
import os
import sys
import django

# إعداد Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from services.models import BankContactRequest, Center
from services.utils.email_service import email_service
from django.utils import timezone

def test_bank_email():
    """اختبار إرسال إيميل مخاطبة البنوك"""
    
    print("=" * 60)
    print("اختبار إرسال إيميل مخاطبة البنوك")
    print("=" * 60)
    print()
    
    # التحقق من إعدادات البريد الإلكتروني
    from django.conf import settings
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("⚠️  تحذير: إعدادات البريد الإلكتروني غير مكتملة!")
        print()
        print("لتفعيل إرسال الإيميلات، قم بإعداد متغيرات البيئة:")
        print("  EMAIL_HOST_USER=your-email@gmail.com")
        print("  EMAIL_HOST_PASSWORD=your-app-password")
        print()
        print("أو قم بتعديل settings.py مباشرة")
        print()
        print("سيتم استخدام Console Backend (الإيميلات ستظهر في Terminal)")
        print()
    else:
        print(f"✅ إعدادات البريد الإلكتروني موجودة:")
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print()
    
    # إنشاء مركز تجريبي
    center, created = Center.objects.get_or_create(
        name='مركز شرطة البحيرة',
        defaults={
            'code': 'BHR',
            'location': 'الشارقة',
            'is_active': True
        }
    )
    
    # إنشاء طلب تجريبي
    print("📝 إنشاء طلب تجريبي...")
    bank_request = BankContactRequest.objects.create(
        center=center,
        report_number='123',
        report_year=2024,
        charge='خيانة الامانة',
        bank_name='بنك ابوظبي التجاري',
        account_number='1234567890',
        status='pending'
    )
    
    print(f"✅ تم إنشاء الطلب رقم: {bank_request.id}")
    print(f"   البنك: {bank_request.bank_name}")
    print(f"   رقم البلاغ: {bank_request.report_number}/{bank_request.report_year}")
    print()
    
    # محاولة إرسال الإيميل
    print("📧 محاولة إرسال الإيميل...")
    print()
    
    try:
        result = email_service.send_bank_contact_request(bank_request)
        
        if result['success']:
            print("✅ نجح إرسال الإيميل!")
            print(f"   الرسالة: {result.get('message', '')}")
        else:
            print("❌ فشل إرسال الإيميل")
            print(f"   السبب: {result.get('message', 'غير محدد')}")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("انتهى الاختبار")
    print("=" * 60)
    
    # حذف الطلب التجريبي (اختياري)
    # bank_request.delete()
    # print("🗑️  تم حذف الطلب التجريبي")

if __name__ == '__main__':
    test_bank_email()

