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
                'name': 'مركز شرطة واسط الشامل',
                'code': 'WST001',
                'location': 'واسط، الشارقة',
                'phone': '+971-6-528-8888',
                'email': 'wasit@shj.police.ae'
            },
            {
                'name': 'مركز شرطة الغرب الشامل',
                'code': 'GRB001',
                'location': 'الغرب، الشارقة',
                'phone': '+971-6-563-3333',
                'email': 'gharb@shj.police.ae'
            },
            {
                'name': 'مركز شرطة البحيرة الشامل',
                'code': 'BHR001',
                'location': 'البحيرة، الشارقة',
                'phone': '+971-6-531-1111',
                'email': 'buhaira@shj.police.ae'
            },
            {
                'name': 'مركز شرطة الصناعية الشامل',
                'code': 'SNA001',
                'location': 'الصناعية، الشارقة',
                'phone': '+971-6-532-2222',
                'email': 'sinaiya@shj.police.ae'
            },
            {
                'name': 'مركز شرطة الصجعة الشامل',
                'code': 'SJA001',
                'location': 'الصجعة، الشارقة',
                'phone': '+971-6-533-3333',
                'email': 'sajaa@shj.police.ae'
            },
            {
                'name': 'مركز شرطة السيوح الشامل',
                'code': 'SYH001',
                'location': 'السيوح، الشارقة',
                'phone': '+971-6-534-4444',
                'email': 'sayouh@shj.police.ae'
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
        
        # ========== إنشاء استعلامات تجريبية ==========
        from services.models import Inquiry
        from django.utils import timezone
        
        sample_inquiries = [
            {
                'inquiry_type': 'report_status',
                'police_center': 'مركز شرطة واسط الشامل',
                'report_number': '1234',
                'report_year': '2024',
                'phone': 'test1@example.com',
                'message': 'استعلام عن بلاغ رقم 1234/2024 في مركز شرطة واسط الشامل'
            },
            {
                'inquiry_type': 'report_status',
                'police_center': 'مركز شرطة الغرب الشامل',
                'report_number': '5678',
                'report_year': '2024',
                'phone': 'test2@example.com',
                'message': 'استعلام عن بلاغ رقم 5678/2024 في مركز شرطة الغرب الشامل'
            },
            {
                'inquiry_type': 'report_status',
                'police_center': 'مركز شرطة البحيرة الشامل',
                'report_number': '9012',
                'report_year': '2024',
                'phone': 'test3@example.com',
                'message': 'استعلام عن بلاغ رقم 9012/2024 في مركز شرطة البحيرة الشامل',
                'is_resolved': True,
                'response': 'تم حل البلاغ بنجاح. شكراً لكم.'
            }
        ]
        
        inquiries_created = 0
        for inquiry_data in sample_inquiries:
            inquiry, created = Inquiry.objects.get_or_create(
                report_number=inquiry_data['report_number'],
                report_year=inquiry_data['report_year'],
                defaults=inquiry_data
            )
            if created:
                inquiries_created += 1
                self.stdout.write(f'  ✅ {inquiry.get_inquiry_id()}')
        
        if inquiries_created > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✅ تم إنشاء {inquiries_created} استعلام تجريبي')
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
        self.stdout.write(f'📊 عدد الاستعلامات: {Inquiry.objects.count()}')
        self.stdout.write('━' * 60)
