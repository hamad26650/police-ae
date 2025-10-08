#!/usr/bin/env python
"""
سكريبت الإعداد التلقائي - يعمل عند كل deploy
يتم تشغيله تلقائياً بعد migrate
"""
import os
import sys
import django

# تفعيل Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import EmployeeProfile, Center

User = get_user_model()

def setup_all():
    """إعداد كل شيء تلقائياً"""
    print("\n" + "="*70)
    print("🚀 الإعداد التلقائي للنظام...")
    print("="*70)
    
    try:
        # 1. إنشاء المركز
        print("\n📍 إنشاء/تحديث المركز...")
        center, created = Center.objects.get_or_create(
            name='مركز شرطة البحيرة',
            defaults={
                'address': 'الشارقة - الإمارات',
                'phone': '+971-6-123-4567',
                'is_active': True
            }
        )
        if created:
            print(f"   ✅ تم إنشاء المركز: {center.name}")
        else:
            print(f"   ℹ️  المركز موجود: {center.name}")
        
        # 2. إنشاء/تحديث حساب الأدمن
        print("\n👨‍💼 إنشاء/تحديث حساب الأدمن...")
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@police.ae',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        if created:
            admin.set_password('Admin@123456')
            admin.save()
            print("   ✅ تم إنشاء حساب الأدمن")
        else:
            if not admin.is_superuser:
                admin.is_superuser = True
                admin.is_staff = True
                admin.save()
            print("   ℹ️  حساب الأدمن موجود")
        
        # 3. إنشاء/تحديث حساب الموظف (12345)
        print("\n👮 إنشاء/تحديث حساب الموظف (12345)...")
        
        # حذف القديم إذا موجود
        User.objects.filter(username='12345').delete()
        
        # إنشاء جديد
        employee_user = User.objects.create_user(
            username='12345',
            password='12345',
            email='employee12345@police.ae',
            first_name='موظف',
            last_name='الشرطة',
            is_staff=True,
            is_active=True
        )
        print(f"   ✅ تم إنشاء المستخدم: {employee_user.username}")
        
        # إنشاء ملف الموظف
        employee_profile = EmployeeProfile.objects.create(
            user=employee_user,
            employee_id='EMP-12345',
            full_name='موظف الشرطة',
            department='قسم البلاغات',
            position='موظف استقبال',
            center=center,
            is_active=True,
            role='staff'
        )
        print(f"   ✅ تم إنشاء ملف الموظف: {employee_profile.full_name}")
        
        # 4. عرض الملخص
        print("\n" + "="*70)
        print("✅ تم الإعداد بنجاح!")
        print("="*70)
        print("\n🔐 الحسابات الجاهزة:")
        print("\n1️⃣ حساب الأدمن:")
        print("   Username: admin")
        print("   Password: Admin@123456")
        print("\n2️⃣ حساب الموظف:")
        print("   Username: 12345")
        print("   Password: 12345")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في الإعداد: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = setup_all()
    sys.exit(0 if success else 1)

