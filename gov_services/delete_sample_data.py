#!/usr/bin/env python
"""
حذف البيانات التجريبية من قاعدة البيانات
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from services.models import Inquiry, ServiceRequest, Center, Service

def delete_sample_data():
    """حذف جميع البيانات التجريبية"""
    
    print("🗑️ حذف البيانات التجريبية...")
    
    # حذف الاستعلامات التجريبية
    sample_inquiries = Inquiry.objects.filter(
        phone__in=['test1@example.com', 'test2@example.com', 'test3@example.com']
    )
    deleted_inquiries = sample_inquiries.count()
    sample_inquiries.delete()
    print(f"✅ تم حذف {deleted_inquiries} استعلام تجريبي")
    
    # حذف الطلبات التجريبية
    sample_requests = ServiceRequest.objects.filter(
        requester_email__contains='@email.com'
    )
    deleted_requests = sample_requests.count()
    sample_requests.delete()
    print(f"✅ تم حذف {deleted_requests} طلب تجريبي")
    
    # عرض الإحصائيات النهائية
    print("\n📊 الإحصائيات النهائية:")
    print(f"📊 عدد الاستعلامات: {Inquiry.objects.count()}")
    print(f"📊 عدد الطلبات: {ServiceRequest.objects.count()}")
    print(f"📊 عدد المراكز: {Center.objects.count()}")
    print(f"📊 عدد الخدمات: {Service.objects.count()}")
    
    print("\n🎉 تم حذف جميع البيانات التجريبية بنجاح!")
    print("النظام الآن جاهز للطلبات الحقيقية فقط.")

if __name__ == '__main__':
    delete_sample_data()
