import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from services.models import Service, SiteSettings

# إضافة الخدمات
services_data = [
    {
        'name': 'prosecution',
        'slug': 'prosecution',
        'description': 'خدمات النيابة العامة والشؤون القانونية والقضائية في إمارة الشارقة',
        'requirements': '''المتطلبات الأساسية:
• صورة من الهوية الإماراتية أو جواز السفر
• المستندات القانونية ذات الصلة
• نموذج الطلب معبأ بالكامل
• رسوم الخدمة (إن وجدت)

الخدمات المتاحة:
• شهادات عدم المحكومية
• التصديق على الوثائق
• الاستعلام عن القضايا
• تقديم الشكاوى القانونية''',
        'fee': 50.00,
        'processing_time': 7,
        'icon': 'fas fa-balance-scale',
        'color': '#8B4513'
    },
    {
        'name': 'digital_id',
        'slug': 'digital_id',
        'description': 'خدمات الهوية الرقمية والتوقيع الإلكتروني والمصادقة الرقمية',
        'requirements': '''المتطلبات الأساسية:
• الهوية الإماراتية الأصلية
• رقم الهاتف المحمول المسجل
• البريد الإلكتروني الشخصي
• صورة شخصية حديثة

الخدمات المتاحة:
• إصدار الهوية الرقمية
• تجديد الهوية الرقمية
• التوقيع الإلكتروني
• المصادقة الرقمية للوثائق''',
        'fee': 100.00,
        'processing_time': 3,
        'icon': 'fas fa-id-card',
        'color': '#007bff'
    },
    {
        'name': 'interior',
        'slug': 'interior',
        'description': 'خدمات وزارة الداخلية للأمن والسلامة والجوازات والإقامة',
        'requirements': '''المتطلبات الأساسية:
• جواز السفر الأصلي
• صور شخصية ملونة
• شهادة طبية معتمدة
• إثبات السكن

الخدمات المتاحة:
• تجديد الإقامة
• إصدار تصاريح العمل
• خدمات الجوازات
• تصاريح السفر للقصر''',
        'fee': 200.00,
        'processing_time': 10,
        'icon': 'fas fa-shield-alt',
        'color': '#28a745'
    },
    {
        'name': 'sharjah_police',
        'slug': 'sharjah_police',
        'description': 'خدمات شرطة الشارقة للمرور والمخالفات والحوادث والتراخيص',
        'requirements': '''المتطلبات الأساسية:
• رخصة القيادة الأصلية
• استمارة التأمين
• فحص المركبة الدوري
• إثبات الهوية

الخدمات المتاحة:
• تجديد رخصة القيادة
• دفع المخالفات المرورية
• تسجيل المركبات
• استخراج تقارير الحوادث''',
        'fee': 75.00,
        'processing_time': 5,
        'icon': 'fas fa-car',
        'color': '#dc3545'
    },
    {
        'name': 'sharjah_municipality',
        'slug': 'sharjah_municipality',
        'description': 'خدمات بلدية الشارقة للبناء والتراخيص والصحة العامة والبيئة',
        'requirements': '''المتطلبات الأساسية:
• المخططات المعمارية المعتمدة
• شهادة ملكية الأرض
• موافقة الدفاع المدني
• تقرير دراسة التربة

الخدمات المتاحة:
• رخص البناء والهدم
• تراخيص الأنشطة التجارية
• شهادات الصحة العامة
• تصاريح الفعاليات''',
        'fee': 300.00,
        'processing_time': 14,
        'icon': 'fas fa-building',
        'color': '#fd7e14'
    }
]

# إضافة الخدمات إلى قاعدة البيانات
for service_data in services_data:
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    if created:
        print(f"تم إضافة خدمة: {dict(Service.SERVICE_TYPES)[service_data['name']]}")
    else:
        print(f"الخدمة موجودة بالفعل: {dict(Service.SERVICE_TYPES)[service_data['name']]}")

# إضافة إعدادات الموقع
site_settings, created = SiteSettings.objects.get_or_create(
    defaults={
        'site_name': 'بوابة الخدمات الحكومية - إمارة الشارقة',
        'site_description': 'بوابة موحدة لجميع الخدمات الحكومية في إمارة الشارقة',
        'contact_email': 'info@sharjah.gov.ae',
        'contact_phone': '06-5555555',
        'address': 'إمارة الشارقة، دولة الإمارات العربية المتحدة',
        'working_hours': 'الأحد - الخميس: 8:00 صباحاً - 2:00 ظهراً'
    }
)

if created:
    print("تم إضافة إعدادات الموقع")
else:
    print("إعدادات الموقع موجودة بالفعل")

print("\nتم الانتهاء من إضافة البيانات التجريبية!")