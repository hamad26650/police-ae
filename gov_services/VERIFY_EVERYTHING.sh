#!/bin/bash
# سكريبت التحقق النهائي - يفحص كل شي

echo "========================================================================"
echo "🔍 فحص شامل للنظام - التحقق من كل شي"
echo "========================================================================"

# 1. فحص الإيميل
echo ""
echo "📧 1️⃣ فحص إعدادات الإيميل..."
echo "------------------------------------------------------------------------"
python CHECK_EMAIL_NOW.py

echo ""
echo "========================================================================"
echo "📊 2️⃣ فحص قاعدة البيانات..."
echo "------------------------------------------------------------------------"
python manage.py shell << EOF
from services.models import Center, EmployeeProfile, Inquiry
from django.contrib.auth import get_user_model
User = get_user_model()

print("✅ المراكز:", Center.objects.count())
print("✅ الموظفين:", EmployeeProfile.objects.count())
print("✅ الاستعلامات:", Inquiry.objects.count())

# تحقق من حساب 12345
try:
    emp = User.objects.get(username='12345')
    print(f"✅ حساب الموظف 12345: موجود")
    print(f"   - is_staff: {emp.is_staff}")
    print(f"   - is_active: {emp.is_active}")
except:
    print("❌ حساب الموظف 12345: غير موجود!")

# تحقق من Admin
try:
    admin = User.objects.get(username='admin')
    print(f"✅ حساب Admin: موجود")
    print(f"   - is_superuser: {admin.is_superuser}")
except:
    print("❌ حساب Admin: غير موجود!")

EOF

echo ""
echo "========================================================================"
echo "🌐 3️⃣ روابط الصفحات:"
echo "------------------------------------------------------------------------"
echo "🏠 الرئيسية: https://buhairah-oqh9h.ondigitalocean.app/"
echo "👮 تسجيل دخول الموظف: https://buhairah-oqh9h.ondigitalocean.app/staff/login/"
echo "📊 Dashboard: https://buhairah-oqh9h.ondigitalocean.app/staff/dashboard/"
echo "🔐 Admin: https://buhairah-oqh9h.ondigitalocean.app/admin/"
echo ""
echo "👤 حساب الموظف: 12345 / 12345"
echo "👨‍💼 حساب Admin: admin / Admin@123456"

echo ""
echo "========================================================================"
echo "✅ انتهى الفحص!"
echo "========================================================================"

