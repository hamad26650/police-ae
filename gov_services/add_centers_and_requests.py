#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from services.models import Service, ServiceRequest, Center
from django.contrib.auth.models import User

def create_centers():
    """إنشاء مراكز تجريبية"""
    centers_data = [
        {
            'name': 'مركز الخدمات الحكومية - الرياض',
            'code': 'RYD001',
            'location': 'شارع الملك فهد، الرياض',
            'phone': '0112345678',
            'email': 'riyadh@gov.sa'
        },
        {
            'name': 'مركز الخدمات الحكومية - جدة',
            'code': 'JED001',
            'location': 'شارع الأمير محمد بن عبدالعزيز، جدة',
            'phone': '0122345678',
            'email': 'jeddah@gov.sa'
        },
        {
            'name': 'مركز الخدمات الحكومية - الدمام',
            'code': 'DMM001',
            'location': 'شارع الملك عبدالعزيز، الدمام',
            'phone': '0132345678',
            'email': 'dammam@gov.sa'
        },
        {
            'name': 'مركز الخدمات الحكومية - مكة المكرمة',
            'code': 'MKK001',
            'location': 'شارع إبراهيم الخليل، مكة المكرمة',
            'phone': '0122567890',
            'email': 'makkah@gov.sa'
        }
    ]
    
    created_centers = 0
    for center_data in centers_data:
        center, created = Center.objects.get_or_create(
            name=center_data['name'],
            defaults=center_data
        )
        if created:
            print(f"تم إنشاء مركز: {center.name}")
            created_centers += 1
        else:
            print(f"المركز موجود مسبقاً: {center.name}")
    
    print(f"تم إنشاء {created_centers} مركز جديد")
    return Center.objects.all()

def create_test_requests():
    """إنشاء طلبات تجريبية للنظام"""
    
    # إنشاء المراكز أولاً
    centers = create_centers()
    
    # الحصول على الخدمات المتاحة
    services = Service.objects.all()
    
    if not services.exists():
        print("لا توجد خدمات في النظام. يرجى إضافة خدمات أولاً.")
        return
    
    # بيانات الطلبات التجريبية
    test_requests = [
        {
            'requester_name': 'أحمد محمد علي',
            'requester_email': 'ahmed.mohamed@email.com',
            'requester_phone': '0501234567',
            'requester_national_id': '1234567890',
            'status': 'pending',
            'priority': 'high',
            'description': 'طلب استخراج شهادة ميلاد عاجل لإجراءات السفر'
        },
        {
            'requester_name': 'فاطمة أحمد السالم',
            'requester_email': 'fatima.salem@email.com',
            'requester_phone': '0509876543',
            'requester_national_id': '0987654321',
            'status': 'in_progress',
            'priority': 'medium',
            'description': 'طلب تجديد الهوية الوطنية'
        },
        {
            'requester_name': 'محمد عبدالله الأحمد',
            'requester_email': 'mohammed.ahmed@email.com',
            'requester_phone': '0551122334',
            'requester_national_id': '1122334455',
            'status': 'completed',
            'priority': 'low',
            'description': 'طلب شهادة حسن سيرة وسلوك'
        },
        {
            'requester_name': 'نورا سعد المطيري',
            'requester_email': 'nora.mutairi@email.com',
            'requester_phone': '0556677889',
            'requester_national_id': '6677889900',
            'status': 'pending',
            'priority': 'high',
            'description': 'طلب تصديق الشهادات الجامعية'
        },
        {
            'requester_name': 'خالد عبدالرحمن القحطاني',
            'requester_email': 'khalid.qahtani@email.com',
            'requester_phone': '0503344556',
            'requester_national_id': '3344556677',
            'status': 'rejected',
            'priority': 'medium',
            'description': 'طلب استخراج رخصة تجارية',
            'rejection_reason': 'نقص في الوثائق المطلوبة'
        },
        {
            'requester_name': 'سارة محمد الزهراني',
            'requester_email': 'sara.zahrani@email.com',
            'requester_phone': '0507788990',
            'requester_national_id': '7788990011',
            'status': 'in_progress',
            'priority': 'high',
            'description': 'طلب تسجيل مولود جديد'
        },
        {
            'requester_name': 'عبدالعزيز سالم الدوسري',
            'requester_email': 'abdulaziz.dosari@email.com',
            'requester_phone': '0502233445',
            'requester_national_id': '2233445566',
            'status': 'pending',
            'priority': 'medium',
            'description': 'طلب شهادة عدم محكومية'
        },
        {
            'requester_name': 'ريم أحمد الشهري',
            'requester_email': 'reem.shahri@email.com',
            'requester_phone': '0558899001',
            'requester_national_id': '8899001122',
            'status': 'completed',
            'priority': 'low',
            'description': 'طلب تصديق عقد زواج'
        },
        {
            'requester_name': 'عمر محمد العتيبي',
            'requester_email': 'omar.otaibi@email.com',
            'requester_phone': '0504455667',
            'requester_national_id': '4455667788',
            'status': 'pending',
            'priority': 'high',
            'description': 'طلب استخراج جواز سفر عاجل'
        },
        {
            'requester_name': 'هند عبدالله الغامدي',
            'requester_email': 'hind.ghamdi@email.com',
            'requester_phone': '0559900112',
            'requester_national_id': '9900112233',
            'status': 'in_progress',
            'priority': 'medium',
            'description': 'طلب تحديث بيانات الهوية الوطنية'
        },
        {
            'requester_name': 'يوسف علي الحربي',
            'requester_email': 'yousef.harbi@email.com',
            'requester_phone': '0506677889',
            'requester_national_id': '5566778899',
            'status': 'pending',
            'priority': 'low',
            'description': 'طلب شهادة خلو طرف'
        },
        {
            'requester_name': 'منى سعد العنزي',
            'requester_email': 'mona.anzi@email.com',
            'requester_phone': '0557788990',
            'requester_national_id': '6677889900',
            'status': 'rejected',
            'priority': 'medium',
            'description': 'طلب ترخيص مهني',
            'rejection_reason': 'عدم استيفاء الشروط المطلوبة'
        },
        {
            'requester_name': 'طارق محمد الشمري',
            'requester_email': 'tariq.shamri@email.com',
            'requester_phone': '0508899001',
            'requester_national_id': '7788990011',
            'status': 'completed',
            'priority': 'high',
            'description': 'طلب تصديق الوثائق الرسمية'
        },
        {
            'requester_name': 'لينا أحمد الفيصل',
            'requester_email': 'lina.faisal@email.com',
            'requester_phone': '0509900112',
            'requester_national_id': '8899001122',
            'status': 'in_progress',
            'priority': 'medium',
            'description': 'طلب استخراج بدل فاقد للهوية'
        },
        {
            'requester_name': 'ماجد عبدالرحمن السبيعي',
            'requester_email': 'majed.subaie@email.com',
            'requester_phone': '0501122334',
            'requester_national_id': '9900112233',
            'status': 'pending',
            'priority': 'high',
            'description': 'طلب تسجيل شركة جديدة'
        }
    ]
    
    created_count = 0
    
    for i, request_data in enumerate(test_requests):
        try:
            # اختيار خدمة ومركز
            service = services.order_by('?').first()
            center = centers.order_by('?').first()
            
            # إنشاء الطلب
            service_request = ServiceRequest.objects.create(
                service=service,
                center=center,
                requester_name=request_data['requester_name'],
                requester_email=request_data['requester_email'],
                requester_phone=request_data['requester_phone'],
                requester_national_id=request_data['requester_national_id'],
                status=request_data['status'],
                priority=request_data['priority'],
                request_details=request_data['description'],
                notes=request_data.get('rejection_reason', ''),
                created_at=timezone.now() - timedelta(days=i),
                updated_at=timezone.now() - timedelta(hours=i)
            )
            
            # إضافة تاريخ حجز للطلبات المكتملة أو قيد المعالجة
            if request_data['status'] in ['completed', 'in_progress']:
                service_request.reservation_date = timezone.now() + timedelta(days=1 + i)
                service_request.reservation_time = timezone.now().time()
                service_request.save()
            
            print(f"تم إنشاء طلب: {request_data['requester_name']} - {service.name}")
            created_count += 1
            
        except Exception as e:
            print(f"خطأ في إنشاء طلب {request_data['requester_name']}: {str(e)}")
    
    print(f"\nتم إنشاء {created_count} طلب تجريبي بنجاح!")
    print("يمكنك الآن الدخول إلى لوحة تحكم الموظفين لرؤية الطلبات.")
    print(f"إجمالي الطلبات في النظام: {ServiceRequest.objects.count()}")

if __name__ == '__main__':
    create_test_requests()