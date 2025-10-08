#!/usr/bin/env python
"""
حل بسيط وسريع - إنشاء حساب الموظف فوراً
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import EmployeeProfile, Center

User = get_user_model()

print("="*60)
print("🔧 إصلاح سريع...")
print("="*60)

# 1. حذف كل شي قديم
print("\n🗑️ مسح البيانات القديمة...")
User.objects.filter(username='12345').delete()
User.objects.filter(username='admin').delete()

# 2. إنشاء/تحديث المركز
print("\n📍 إنشاء المركز...")
center = Center.objects.create(
    name='مركز شرطة البحيرة',
    address='الشارقة',
    phone='123456',
    is_active=True
)
print(f"✅ المركز: {center.name}")

# 3. إنشاء Admin
print("\n👨‍💼 إنشاء Admin...")
admin = User.objects.create_superuser(
    username='admin',
    email='admin@police.ae',
    password='Admin@123456',
    first_name='Admin',
    last_name='System'
)
print("✅ Admin: admin / Admin@123456")

# 4. إنشاء الموظف
print("\n👮 إنشاء الموظف...")
emp_user = User.objects.create_user(
    username='12345',
    password='12345',
    email='emp@police.ae',
    first_name='موظف',
    last_name='الشرطة',
    is_staff=True,
    is_active=True
)
print("✅ المستخدم: 12345 / 12345")

# 5. إنشاء ملف الموظف
print("\n📋 إنشاء ملف الموظف...")
emp_profile = EmployeeProfile.objects.create(
    user=emp_user,
    employee_id='12345',
    department='البلاغات',
    phone='123456',
    center=center,
    is_active=True,
    role='center'
)
print(f"✅ الملف: {emp_profile.employee_id}")

# 6. اختبار
print("\n🧪 اختبار تسجيل الدخول...")
from django.contrib.auth import authenticate
test = authenticate(username='12345', password='12345')
if test:
    print("✅ تسجيل الدخول يعمل!")
else:
    print("❌ فشل!")

print("\n" + "="*60)
print("✅ تم الإصلاح!")
print("="*60)
print("\n🔐 معلومات الدخول:")
print("   صفحة الموظف: /staff/login/")
print("   اسم المستخدم: 12345")
print("   كلمة المرور: 12345")
print("="*60)

