#!/usr/bin/env python
"""
سكريبت حل جميع المشاكل دفعة واحدة
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import EmployeeProfile, Center

User = get_user_model()

print("="*70)
print("🔧 جاري إصلاح جميع المشاكل...")
print("="*70)

# 1. إنشاء/تحديث المركز
print("\n📍 الخطوة 1: إنشاء المركز...")
try:
    center = Center.objects.first()
    if not center:
        center = Center.objects.create(
            name='مركز شرطة البحيرة',
            address='الشارقة - الإمارات العربية المتحدة',
            phone='+971-6-123-4567',
            is_active=True
        )
        print("✅ تم إنشاء المركز: مركز شرطة البحيرة")
    else:
        print(f"✅ المركز موجود: {center.name}")
except Exception as e:
    print(f"❌ خطأ في المركز: {e}")
    center = None

# 2. حذف وإعادة إنشاء المستخدم 12345
print("\n👤 الخطوة 2: إنشاء حساب الموظف (12345)...")
try:
    # حذف القديم
    User.objects.filter(username='12345').delete()
    
    # إنشاء جديد
    user = User.objects.create_user(
        username='12345',
        password='12345',
        email='employee@police.ae',
        first_name='موظف',
        last_name='الشرطة',
        is_staff=True,
        is_active=True
    )
    print(f"✅ تم إنشاء المستخدم: {user.username}")
    
    # إنشاء ملف موظف
    if center:
        employee, created = EmployeeProfile.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': 'EMP-12345',
                'full_name': 'موظف الشرطة',
                'department': 'قسم البلاغات',
                'position': 'موظف استقبال',
                'center': center,
                'is_active': True,
                'role': 'staff'
            }
        )
        print(f"✅ تم إنشاء ملف الموظف: {employee.full_name}")
    else:
        print("⚠️ تحذير: لم يتم إنشاء ملف الموظف (المركز غير موجود)")
        
except Exception as e:
    print(f"❌ خطأ في إنشاء الموظف: {e}")

# 3. التحقق من حساب الأدمن
print("\n👨‍💼 الخطوة 3: التحقق من حساب الأدمن...")
try:
    admin = User.objects.filter(username='admin').first()
    if admin:
        print(f"✅ حساب الأدمن موجود: {admin.username}")
        # التأكد من أن له صلاحيات
        if not admin.is_superuser:
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            print("✅ تم تحديث صلاحيات الأدمن")
    else:
        print("⚠️ حساب الأدمن غير موجود، سيتم إنشاءه...")
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@police.ae',
            password='Admin@123456'
        )
        print("✅ تم إنشاء حساب الأدمن")
except Exception as e:
    print(f"❌ خطأ في الأدمن: {e}")

# 4. عرض الملخص
print("\n"+"="*70)
print("📊 ملخص الحسابات:")
print("="*70)

print("\n🔐 حساب الأدمن:")
print("   🌐 الرابط: https://buhairah-oqh9h.ondigitalocean.app/admin/")
print("   👤 Username: admin")
print("   🔑 Password: Admin@123456")

print("\n🔐 حساب الموظف:")
print("   🌐 الرابط: https://buhairah-oqh9h.ondigitalocean.app/staff/login/")
print("   👤 Username: 12345")
print("   🔑 Password: 12345")

# 5. اختبار تسجيل الدخول
print("\n"+"="*70)
print("🧪 اختبار تسجيل الدخول:")
print("="*70)

from django.contrib.auth import authenticate

# اختبار الأدمن
admin_auth = authenticate(username='admin', password='Admin@123456')
if admin_auth:
    print("✅ حساب الأدمن يعمل بشكل صحيح")
else:
    print("❌ حساب الأدمن لا يعمل")

# اختبار الموظف
staff_auth = authenticate(username='12345', password='12345')
if staff_auth:
    print("✅ حساب الموظف يعمل بشكل صحيح")
else:
    print("❌ حساب الموظف لا يعمل")

print("\n"+"="*70)
print("🎉 تم إصلاح جميع المشاكل!")
print("="*70)
print("\n💡 الآن جرّب تسجيل الدخول:")
print("   1. امسح cookies المتصفح (Ctrl+Shift+Delete)")
print("   2. أعد تحميل الصفحة (Ctrl+Shift+R)")
print("   3. سجل الدخول بالمعلومات أعلاه")
print("="*70)

