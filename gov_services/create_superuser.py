import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth.models import User

# إنشاء superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@sharjah.gov.ae',
        password='admin123'
    )
    print("تم إنشاء حساب المدير بنجاح!")
    print("اسم المستخدم: admin")
    print("كلمة المرور: admin123")
else:
    print("حساب المدير موجود بالفعل!")