"""
Django management command to create superuser
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'إنشاء حساب مدير (superuser) للنظام'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@police.ae'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'المستخدم {username} موجود بالفعل!')
            )
            # Update password just in case
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'تم تحديث كلمة المرور للمستخدم {username}')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ تم إنشاء حساب المدير بنجاح!')
            )
        
        self.stdout.write('━' * 50)
        self.stdout.write(self.style.SUCCESS('بيانات الدخول:'))
        self.stdout.write(f'  اسم المستخدم: {username}')
        self.stdout.write(f'  كلمة المرور: {password}')
        self.stdout.write('━' * 50)

