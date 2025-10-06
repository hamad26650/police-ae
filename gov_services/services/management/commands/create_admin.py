"""
Django management command to create superuser and initial data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Center, Service, EmployeeProfile


class Command(BaseCommand):
    help = 'إنشاء حساب مدير وبيانات أساسية للنظام'

    def handle(self, *args, **options):
        # ========== إنشاء المستخدم Admin ==========
        username = 'admin'
        email = 'admin@police.ae'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'المستخدم {username} موجود بالفعل!')
            )
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'تم تحديث كلمة المرور للمستخدم {username}')
            )
        else:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ تم إنشاء حساب المدير بنجاح!')
            )
        
        # ========== إنشاء ملف الموظف ==========
        try:
            first_center = Center.objects.first()
            employee_profile, created = EmployeeProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'admin',
                    'department': 'الإدارة العامة',
                    'center': first_center
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✅ تم إنشاء ملف الموظف'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'تحذير: {str(e)}'))
        
        # ========== إنشاء المراكز ==========
        centers_data = [
            {
                'name': 'مركز شرطة البحيرة',
                'code': 'BHR001',
                'location': 'البحيرة، الشارقة',
                'phone': '+971-6-528-8888',
                'email': 'buhaira@shj.police.ae'
            },
            {
                'name': 'مركز شرطة القاسمية',
                'code': 'QAS001',
                'location': 'القاسمية، الشارقة',
                'phone': '+971-6-563-3333',
                'email': 'qasimia@shj.police.ae'
            },
            {
                'name': 'مركز شرطة الخان',
                'code': 'KHN001',
                'location': 'الخان، الشارقة',
                'phone': '+971-6-531-1111',
                'email': 'khan@shj.police.ae'
            },
        ]
        
        centers_created = 0
        for center_data in centers_data:
            center, created = Center.objects.get_or_create(
                code=center_data['code'],
                defaults=center_data
            )
            if created:
                centers_created += 1
                self.stdout.write(f'  ✅ {center.name}')
        
        if centers_created > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✅ تم إنشاء {centers_created} مركز')
            )
        
        # ========== عرض معلومات الدخول ==========
        self.stdout.write('━' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 تم إعداد النظام بنجاح!'))
        self.stdout.write('━' * 60)
        self.stdout.write(self.style.SUCCESS('بيانات الدخول:'))
        self.stdout.write(f'  👤 اسم المستخدم: {username}')
        self.stdout.write(f'  🔑 كلمة المرور: {password}')
        self.stdout.write('━' * 60)
        self.stdout.write(f'📊 عدد المراكز: {Center.objects.count()}')
        self.stdout.write('━' * 60)
