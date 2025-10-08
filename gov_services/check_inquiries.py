#!/usr/bin/env python
"""
فحص الاستعلامات في قاعدة البيانات - هل الإيميلات صحيحة؟
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
import django
django.setup()

from services.models import Inquiry

print("="*80)
print("🔍 فحص الاستعلامات في قاعدة البيانات")
print("="*80)

inquiries = Inquiry.objects.filter(inquiry_type='report_status').order_by('-created_at')[:20]

if not inquiries.exists():
    print("\n❌ لا توجد استعلامات!")
    print("   قدم استعلام جديد من الموقع أولاً.")
    sys.exit(1)

print(f"\n✅ عدد الاستعلامات: {inquiries.count()}")
print("\n📋 آخر 20 استعلام:")
print("="*80)

valid_count = 0
invalid_count = 0

for i, inq in enumerate(inquiries, 1):
    print(f"\n{i}. ID: {inq.id}")
    print(f"   رقم البلاغ: {inq.report_number}/{inq.report_year}")
    print(f"   المركز: {inq.police_center}")
    
    # فحص حقل email
    if inq.email:
        print(f"   ✅ Email field: {inq.email}")
        if '@' in inq.email:
            print(f"      ✅ صحيح - يحتوي على @")
            valid_count += 1
        else:
            print(f"      ❌ غير صحيح - ما فيه @")
            invalid_count += 1
    else:
        print(f"   ⚠️  Email field: فارغ")
    
    # فحص حقل phone
    if inq.phone:
        print(f"   📞 Phone field: {inq.phone}")
        if '@' in inq.phone:
            print(f"      ✅ يحتوي على @ (إيميل)")
            if not inq.email:
                valid_count += 1
        else:
            print(f"      ❌ رقم هاتف - مو إيميل!")
            if not inq.email:
                invalid_count += 1
    else:
        print(f"   ⚠️  Phone field: فارغ")
    
    # الإيميل النهائي اللي راح يستخدم
    final_email = inq.email if inq.email else inq.phone
    print(f"   → الإيميل المستخدم: {final_email}")
    
    if final_email and '@' in final_email:
        print(f"   ✅ راح يُرسل لهذا الإيميل")
    else:
        print(f"   ❌ لن يُرسل - الإيميل غير صحيح!")
    
    print(f"   الحالة: {inq.get_status_display()}")
    print(f"   تم الرد: {'نعم' if inq.is_resolved else 'لا'}")
    print("-"*80)

print("\n" + "="*80)
print("📊 الملخص:")
print("="*80)
print(f"✅ استعلامات مع إيميل صحيح: {valid_count}")
print(f"❌ استعلامات مع إيميل غير صحيح: {invalid_count}")

if invalid_count > 0:
    print("\n⚠️  تحذير:")
    print(f"   {invalid_count} استعلام يحتوي على رقم هاتف بدلاً من إيميل!")
    print("\n💡 الحل:")
    print("   1. قدم استعلام جديد من الموقع")
    print("   2. في خانة 'البريد الإلكتروني' أدخل إيميل صحيح:")
    print("      ✅ مثال: customer@example.com")
    print("      ❌ مو: 0501234567")

if valid_count == 0:
    print("\n❌ لا توجد استعلامات بإيميل صحيح!")
    print("   لازم تقدم استعلام جديد مع إيميل صحيح.")
else:
    print(f"\n✅ يوجد {valid_count} استعلام يمكن إرسال إيميل له.")

print("="*80)

