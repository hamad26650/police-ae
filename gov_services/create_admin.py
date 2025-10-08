#!/usr/bin/env python
"""
سكريبت لإنشاء مستخدم admin تلقائياً
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# معلومات Admin
username = 'admin'
email = 'admin@police.ae'
password = 'Admin@123456'  # غيّرها بعدين من /admin/

# إنشاء Admin إذا مو موجود
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ تم إنشاء مستخدم Admin: {username}")
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    print("\n⚠️ غيّر كلمة المرور من لوحة الإدارة!")
else:
    print(f"⚠️ المستخدم {username} موجود بالفعل")

