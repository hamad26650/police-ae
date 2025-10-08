#!/usr/bin/env python
"""
سكريبت لإنشاء حساب موظف تلقائياً
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import EmployeeProfile

User = get_user_model()

# معلومات الموظف
username = 'employee1'
email = 'employee1@police.ae'
password = 'Employee@123'  # غيّرها بعدين
employee_id = 'EMP001'
full_name = 'موظف الشرطة الأول'
department = 'قسم البلاغات'
position = 'موظف استقبال'

print("🔄 جاري إنشاء حساب الموظف...")

# إنشاء User إذا مو موجود
if User.objects.filter(username=username).exists():
    print(f"⚠️ المستخدم {username} موجود بالفعل!")
    user = User.objects.get(username=username)
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ تم إنشاء مستخدم: {username}")

# إنشاء Employee Profile إذا مو موجود
if EmployeeProfile.objects.filter(user=user).exists():
    print(f"⚠️ الموظف مسجل بالفعل!")
    employee = EmployeeProfile.objects.get(user=user)
else:
    employee = EmployeeProfile.objects.create(
        user=user,
        employee_id=employee_id,
        full_name=full_name,
        department=department,
        position=position,
        is_active=True
    )
    print(f"✅ تم إنشاء ملف الموظف")

print("\n" + "="*50)
print("🎉 تم إنشاء حساب الموظف بنجاح!")
print("="*50)
print(f"\n📋 معلومات تسجيل الدخول:")
print(f"   Username: {username}")
print(f"   Password: {password}")
print(f"   Email: {email}")
print(f"\n👤 معلومات الموظف:")
print(f"   الرقم الوظيفي: {employee_id}")
print(f"   الاسم الكامل: {full_name}")
print(f"   القسم: {department}")
print(f"   المنصب: {position}")
print(f"\n🔗 رابط تسجيل الدخول:")
print(f"   https://buhairah-oqh9h.ondigitalocean.app/staff/login/")
print(f"\n⚠️ تذكير: غيّر كلمة المرور بعد أول تسجيل دخول!")
print("="*50)

