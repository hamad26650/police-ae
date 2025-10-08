#!/usr/bin/env python
"""
سكريبت سريع لإنشاء موظف وتجهيز النظام
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import EmployeeProfile, Center

User = get_user_model()

print("🔄 جاري إنشاء النظام...")

# إنشاء مركز إذا لم يكن موجود
center, created = Center.objects.get_or_create(
    name='مركز شرطة البحيرة',
    defaults={
        'address': 'الشارقة',
        'phone': '+971-6-123-4567',
        'is_active': True
    }
)
if created:
    print(f"✅ تم إنشاء المركز: {center.name}")
else:
    print(f"ℹ️ المركز موجود: {center.name}")

# حذف المستخدم القديم إذا كان موجود
if User.objects.filter(username='12345').exists():
    User.objects.filter(username='12345').delete()
    print("🗑️ تم حذف المستخدم القديم")

# إنشاء مستخدم جديد
user = User.objects.create_user(
    username='12345',
    password='12345',
    email='employee@police.ae',
    is_staff=True,
    is_active=True
)
print(f"✅ تم إنشاء المستخدم: {user.username}")

# إنشاء ملف موظف
employee = EmployeeProfile.objects.create(
    user=user,
    employee_id='12345',
    full_name='موظف الشرطة',
    department='قسم البلاغات',
    position='موظف استقبال',
    center=center,
    is_active=True
)
print(f"✅ تم إنشاء ملف الموظف: {employee.full_name}")

print("\n" + "="*50)
print("🎉 تم الإعداد بنجاح!")
print("="*50)
print(f"\n📋 معلومات تسجيل الدخول:")
print(f"   🌐 الرابط: https://buhairah-oqh9h.ondigitalocean.app/staff/login/")
print(f"   👤 Username: 12345")
print(f"   🔑 Password: 12345")
print(f"\n✅ جاهز للاستخدام!")
print("="*50)

