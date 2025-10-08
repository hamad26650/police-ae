#!/usr/bin/env python
"""
سكريبت إنشاء موظف - اسم: 12345 | رمز: 12345
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import EmployeeProfile, Center

User = get_user_model()

print("=" * 60)
print("🔄 جاري إنشاء حساب الموظف...")
print("=" * 60)

# 1. إنشاء المركز
center, created = Center.objects.get_or_create(
    name='مركز شرطة البحيرة',
    defaults={
        'address': 'الشارقة - الإمارات',
        'phone': '+971-6-123-4567',
        'is_active': True
    }
)
print(f"{'✅ تم إنشاء المركز' if created else 'ℹ️  المركز موجود'}: {center.name}")

# 2. حذف الحساب القديم إذا موجود
if User.objects.filter(username='12345').exists():
    old_user = User.objects.get(username='12345')
    # حذف ملف الموظف المرتبط
    EmployeeProfile.objects.filter(user=old_user).delete()
    # حذف المستخدم
    old_user.delete()
    print("🗑️  تم حذف الحساب القديم")

# 3. إنشاء المستخدم الجديد
user = User.objects.create_user(
    username='12345',
    password='12345',
    email='employee12345@police.ae',
    first_name='موظف',
    last_name='الشرطة',
    is_staff=True,
    is_active=True
)
print(f"✅ تم إنشاء المستخدم: {user.username}")
print(f"   📧 Email: {user.email}")
print(f"   🔐 Password: 12345")
print(f"   ✔️  is_staff: {user.is_staff}")
print(f"   ✔️  is_active: {user.is_active}")

# 4. إنشاء ملف الموظف
employee = EmployeeProfile.objects.create(
    user=user,
    employee_id='EMP-12345',
    full_name='موظف الشرطة',
    department='قسم البلاغات والاستعلامات',
    position='موظف استقبال',
    center=center,
    is_active=True,
    role='staff'
)
print(f"✅ تم إنشاء ملف الموظف")
print(f"   🆔 الرقم الوظيفي: {employee.employee_id}")
print(f"   👤 الاسم: {employee.full_name}")
print(f"   🏢 القسم: {employee.department}")
print(f"   💼 المنصب: {employee.position}")
print(f"   📍 المركز: {employee.center.name}")

print("\n" + "=" * 60)
print("🎉 تم إنشاء حساب الموظف بنجاح!")
print("=" * 60)
print(f"\n🔐 معلومات تسجيل الدخول:")
print(f"   🌐 الصفحة: https://buhairah-oqh9h.ondigitalocean.app/staff/login/")
print(f"   👤 الاسم: 12345")
print(f"   🔑 الرمز: 12345")
print(f"\n💡 ملاحظة:")
print(f"   - استخدم هذه المعلومات لتسجيل الدخول")
print(f"   - يمكنك تغيير كلمة المرور لاحقاً من لوحة التحكم")
print("=" * 60)

# 5. التحقق من الإنشاء
try:
    from django.contrib.auth import authenticate
    auth_user = authenticate(username='12345', password='12345')
    if auth_user:
        print("\n✅ تم التحقق: الاسم والرمز يعملان بشكل صحيح!")
    else:
        print("\n⚠️  تحذير: فشل التحقق من الحساب")
except Exception as e:
    print(f"\n⚠️  خطأ في التحقق: {str(e)}")

print("\n🚀 جاهز للاستخدام الآن!")

