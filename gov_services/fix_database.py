#!/usr/bin/env python
"""
إصلاح قاعدة البيانات - يشتغل حتى لو فيه أخطاء
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import Center, EmployeeProfile

User = get_user_model()

print("="*60)
print("🔧 إصلاح قاعدة البيانات...")
print("="*60)

try:
    # 1. حذف البيانات القديمة
    print("\n🗑️ مسح البيانات القديمة...")
    User.objects.filter(username__in=['admin', '12345']).delete()
    Center.objects.all().delete()
    print("✅ تم المسح")
    
    # 2. إنشاء المركز
    print("\n📍 إنشاء المركز...")
    center = Center.objects.create(
        name='مركز شرطة البحيرة',
        address='الشارقة - الإمارات',
        phone='+971-6-123-4567',
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
    
    # ملف موظف للأدمن
    EmployeeProfile.objects.create(
        user=admin,
        employee_id='ADMIN-001',
        department='الإدارة العامة',
        phone='+971-50-000-0001',
        center=center,
        is_active=True,
        role='admin'
    )
    print("✅ Admin: admin / Admin@123456")
    
    # 4. إنشاء الموظف
    print("\n👮 إنشاء الموظف...")
    emp = User.objects.create_user(
        username='12345',
        password='12345',
        email='emp@police.ae',
        first_name='موظف',
        last_name='الشرطة',
        is_staff=True,
        is_active=True
    )
    
    # ملف موظف
    EmployeeProfile.objects.create(
        user=emp,
        employee_id='EMP-12345',
        department='قسم البلاغات',
        phone='+971-50-123-4567',
        center=center,
        is_active=True,
        role='center'
    )
    print("✅ الموظف: 12345 / 12345")
    
    # 5. اختبار
    print("\n🧪 اختبار...")
    from django.contrib.auth import authenticate
    
    test_admin = authenticate(username='admin', password='Admin@123456')
    test_emp = authenticate(username='12345', password='12345')
    
    if test_admin and test_emp:
        print("✅ جميع الحسابات تعمل!")
    else:
        print("⚠️ بعض الحسابات لا تعمل")
    
    print("\n" + "="*60)
    print("✅ تم الإصلاح بنجاح!")
    print("="*60)
    print("\n🔐 معلومات الدخول:")
    print("\n1️⃣ Admin:")
    print("   🌐 /admin/")
    print("   👤 admin")
    print("   🔑 Admin@123456")
    print("\n2️⃣ الموظف:")
    print("   🌐 /staff/login/")
    print("   👤 12345")
    print("   🔑 12345")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ خطأ: {e}")
    import traceback
    traceback.print_exc()

