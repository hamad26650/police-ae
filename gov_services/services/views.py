from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import Service, SiteSettings, ServiceRequest, EmployeeProfile, Center, SMSMessage, Inquiry
from .forms import InquiryForm, StaffLoginForm, InquiryResponseForm
from .decorators import rate_limit, track_failed_login, log_user_activity, get_client_ip
from .utils.email_service import email_service
import logging

# إعداد Logger
logger = logging.getLogger('services')

def home(request):
    """الصفحة الرئيسية"""
    services = Service.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    context = {
        'services': services,
        'site_settings': site_settings,
    }
    return render(request, 'services/home.html', context)

def test_page(request):
    """صفحة اختبار بسيطة للتأكد من عمل الخادم"""
    return render(request, 'services/test.html')



# النيابة العامة
def prosecution(request):
    """صفحة النيابة العامة"""
    return render(request, 'services/prosecution.html')

def petition_number(request):
    """صفحة استخراج رقم العريضة"""
    return render(request, 'services/petition_number.html')

def submit_petition(request):
    """صفحة تقديم عريضة النيابة"""
    return render(request, 'services/submit_petition.html')

# الهوية الرقمية
def digital_identity(request):
    """صفحة الهوية الرقمية"""
    return render(request, 'services/digital_identity.html')

# وزارة الداخلية
def interior_ministry(request):
    """صفحة وزارة الداخلية"""
    return render(request, 'services/interior_ministry.html')

# نموذج 1
def model1(request):
    """صفحة نموذج 1"""
    return render(request, 'services/model1.html')

def submit_report(request):
    """صفحة تقديم البلاغ الإلكتروني"""
    return render(request, 'services/submit_report.html')

@rate_limit(key_prefix='inquiry', limit=3, period=600)  # 3 محاولات كل 10 دقائق
def check_report_status(request):
    """صفحة الاستعلام عن حالة البلاغ"""
    form = InquiryForm()
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        
        if form.is_valid():
            # الحصول على البيانات المنظفة والمحققة
            police_center = form.cleaned_data['police_center']
            report_number = form.cleaned_data['report_number']
            report_year = form.cleaned_data['report_year']
            email = form.cleaned_data['email']
            
            # الحصول على IP
            ip = get_client_ip(request)
            
            # حفظ الاستعلام في قاعدة البيانات
            inquiry = Inquiry.objects.create(
                inquiry_type='report_status',
                police_center=police_center,
                report_number=str(report_number),
                report_year=str(report_year),
                phone=email,  # نستخدم حقل phone لحفظ الإيميل
                message=f"استعلام عن بلاغ رقم {report_number}/{report_year} في {police_center}"
            )
            
            logger.info(f'استعلام جديد: {inquiry.get_inquiry_id()} - الإيميل: {email} - IP: {ip}')
            messages.success(request, f'تم استلام طلب الاستعلام برقم {inquiry.get_inquiry_id()} وسيتم التواصل معكم قريباً عبر البريد الإلكتروني {email}')
            return redirect('services:check_report_status')
        else:
            # عرض أخطاء النموذج
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    
    context = {'form': form}
    return render(request, 'services/check_report_status.html', context)

# ========== نظام الموظفين ==========

@track_failed_login(max_attempts=5, lockout_time=900)  # 5 محاولات، قفل 15 دقيقة
@rate_limit(key_prefix='staff_login', limit=10, period=600)  # 10 محاولات كل 10 دقائق
def staff_login(request):
    """صفحة تسجيل دخول الموظفين"""
    if request.user.is_authenticated:
        return redirect('services:staff_dashboard')
    
    form = StaffLoginForm()
    
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # التحقق من أن المستخدم موظف أو مدير
                if user.is_superuser or user.is_staff:
                    # إنشاء ملف شخصي إذا لم يكن موجوداً للمدراء
                    if user.is_superuser:
                        employee_profile, created = EmployeeProfile.objects.get_or_create(
                            user=user,
                            defaults={
                                'role': 'admin',
                                'department': 'الإدارة العامة',
                                'center': Center.objects.first() if Center.objects.exists() else None
                            }
                        )
                    login(request, user)
                    logger.info(f'تسجيل دخول ناجح: {username} من IP: {get_client_ip(request)}')
                    messages.success(request, f'مرحباً {user.get_full_name() or user.username}')
                    return redirect('services:staff_dashboard')
                else:
                    # التحقق من وجود ملف شخصي للموظفين العاديين
                    try:
                        employee_profile = EmployeeProfile.objects.get(user=user)
                        login(request, user)
                        logger.info(f'تسجيل دخول موظف: {username} من IP: {get_client_ip(request)}')
                        messages.success(request, f'مرحباً {user.get_full_name() or user.username}')
                        return redirect('services:staff_dashboard')
                    except EmployeeProfile.DoesNotExist:
                        logger.warning(f'محاولة دخول غير مصرح بها: {username} من IP: {get_client_ip(request)}')
                        messages.error(request, 'هذا الحساب غير مخول للدخول إلى نظام الموظفين')
    
    context = {'form': form}
    return render(request, 'services/staff_login.html', context)

def staff_logout(request):
    """تسجيل خروج الموظفين"""
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('services:staff_login')

@login_required(login_url='services:staff_login')
def staff_dashboard(request):
    """لوحة تحكم الموظفين"""
    # التحقق من الصلاحيات
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'غير مخول للوصول')
        return redirect('services:staff_login')
    
    # محاولة الحصول على ملف الموظف أو إنشاؤه للمدراء
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
    except EmployeeProfile.DoesNotExist:
        if request.user.is_superuser:
            # إنشاء ملف شخصي للمدير
            employee_profile = EmployeeProfile.objects.create(
                user=request.user,
                department='الإدارة العامة',
                role='admin',
                center=Center.objects.first() if Center.objects.exists() else None
            )
        else:
            messages.error(request, 'غير مخول للوصول')
            return redirect('services:staff_login')
    
    # جلب الاستعلامات عن البلاغات (جميع الموظفين يرون جميع الاستعلامات)
    inquiries = Inquiry.objects.filter(inquiry_type='report_status').order_by('-created_at')
    
    # فلترة حسب الحالة إذا تم تحديدها
    status_filter = request.GET.get('status')
    if status_filter == 'resolved':
        inquiries = inquiries.filter(is_resolved=True)
    elif status_filter == 'pending':
        inquiries = inquiries.filter(is_resolved=False)
    
    # البحث في النص
    search_query = request.GET.get('search')
    if search_query:
        inquiries = inquiries.filter(
            Q(phone__icontains=search_query) |
            Q(report_number__icontains=search_query) |
            Q(police_center__icontains=search_query)
        )
    
    # إحصائيات
    total_inquiries = inquiries.count()
    pending_inquiries = inquiries.filter(is_resolved=False).count()
    resolved_inquiries = inquiries.filter(is_resolved=True).count()
    
    context = {
        'employee_profile': employee_profile,
        'inquiries': inquiries,
        'current_status': status_filter,
        'search_query': search_query,
        'total_inquiries': total_inquiries,
        'pending_inquiries': pending_inquiries,
        'resolved_inquiries': resolved_inquiries,
    }
    
    return render(request, 'services/staff_dashboard.html', context)

@login_required(login_url='services:staff_login')
def update_request_status(request, request_id):
    """تحديث حالة الطلب"""
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
        service_request = ServiceRequest.objects.get(id=request_id)
        
        # التحقق من الصلاحية
        if employee_profile.role != 'admin' and service_request.center != employee_profile.center:
            messages.error(request, 'غير مخول لتعديل هذا الطلب')
            return redirect('services:staff_dashboard')
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(ServiceRequest.STATUS_CHOICES):
                service_request.status = new_status
                service_request.save()
                messages.success(request, 'تم تحديث حالة الطلب بنجاح')
            else:
                messages.error(request, 'حالة غير صحيحة')
        
    except (EmployeeProfile.DoesNotExist, ServiceRequest.DoesNotExist):
        messages.error(request, 'خطأ في الوصول للبيانات')
    
    return redirect('services:staff_dashboard')

@login_required(login_url='services:staff_login')
def reserve_request(request, request_id):
    """حجز طلب من قبل موظف"""
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        
        # التحقق من الصلاحية
        if employee_profile.role != 'admin' and service_request.center != employee_profile.center:
            return JsonResponse({'success': False, 'message': 'غير مخول للوصول لهذا الطلب'})
        
        # التحقق من إمكانية الحجز
        if not service_request.can_be_reserved_by(request.user):
            return JsonResponse({'success': False, 'message': 'لا يمكن حجز هذا الطلب'})
        
        # حجز الطلب
        service_request.reserved_by = request.user
        service_request.reserved_at = timezone.now()
        service_request.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'تم حجز الطلب بنجاح',
            'reserved_by': request.user.get_full_name() or request.user.username
        })
        
    except EmployeeProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'خطأ في الوصول للبيانات'})

@login_required(login_url='services:staff_login')
def release_request(request, request_id):
    """إلغاء حجز طلب"""
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        
        # التحقق من الصلاحية
        if employee_profile.role != 'admin' and service_request.center != employee_profile.center:
            return JsonResponse({'success': False, 'message': 'غير مخول للوصول لهذا الطلب'})
        
        # التحقق من أن المستخدم هو من حجز الطلب أو أنه admin
        if service_request.reserved_by != request.user and employee_profile.role != 'admin':
            return JsonResponse({'success': False, 'message': 'لا يمكنك إلغاء حجز طلب محجوز من قبل موظف آخر'})
        
        # إلغاء الحجز
        service_request.reserved_by = None
        service_request.reserved_at = None
        service_request.save()
        
        return JsonResponse({'success': True, 'message': 'تم إلغاء حجز الطلب بنجاح'})
        
    except EmployeeProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'خطأ في الوصول للبيانات'})

@login_required(login_url='services:staff_login')
def send_sms(request, request_id):
    """إرسال رسالة نصية لمقدم الطلب"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'طريقة غير مسموحة'})
    
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        
        # التحقق من الصلاحية
        if employee_profile.role != 'admin' and service_request.center != employee_profile.center:
            return JsonResponse({'success': False, 'message': 'غير مخول للوصول لهذا الطلب'})
        
        # التحقق من أن الطلب محجوز من قبل المستخدم الحالي
        if service_request.reserved_by != request.user:
            return JsonResponse({'success': False, 'message': 'يجب حجز الطلب أولاً لإرسال رسالة'})
        
        message_text = request.POST.get('message', '').strip()
        if not message_text:
            return JsonResponse({'success': False, 'message': 'نص الرسالة مطلوب'})
        
        # إنشاء رسالة نصية
        sms_message = SMSMessage.objects.create(
            request=service_request,
            sender=request.user,
            message=message_text,
            phone_number=service_request.requester_phone,
            is_sent=True  # في التطبيق الحقيقي، سيتم الإرسال عبر API
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'تم إرسال الرسالة النصية بنجاح',
            'sms_id': sms_message.id
        })
        
    except EmployeeProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'خطأ في الوصول للبيانات'})

@login_required(login_url='services:staff_login')
def reject_request(request, request_id):
    """رفض طلب مع إرسال رسالة"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'طريقة غير مسموحة'})
    
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        
        # التحقق من الصلاحية
        if employee_profile.role != 'admin' and service_request.center != employee_profile.center:
            return JsonResponse({'success': False, 'message': 'غير مخول للوصول لهذا الطلب'})
        
        # التحقق من أن الطلب محجوز من قبل المستخدم الحالي
        if service_request.reserved_by != request.user:
            return JsonResponse({'success': False, 'message': 'يجب حجز الطلب أولاً لرفضه'})
        
        rejection_reason = request.POST.get('reason', '').strip()
        if not rejection_reason:
            return JsonResponse({'success': False, 'message': 'سبب الرفض مطلوب'})
        
        # تحديث حالة الطلب إلى مرفوض
        service_request.status = 'rejected'
        service_request.notes = f"مرفوض: {rejection_reason}"
        service_request.save()
        
        # إرسال رسالة نصية بالرفض
        sms_message = SMSMessage.objects.create(
            request=service_request,
            sender=request.user,
            message=f"تم رفض طلبكم رقم {service_request.get_request_id()}. السبب: {rejection_reason}",
            phone_number=service_request.requester_phone,
            is_sent=True
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'تم رفض الطلب وإرسال إشعار للمتقدم',
            'new_status': 'مرفوض'
        })
        
    except EmployeeProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'خطأ في الوصول للبيانات'})

# ========== نظام الاستعلامات ==========

@login_required(login_url='services:staff_login')
@log_user_activity('respond_to_inquiry')
def respond_to_inquiry(request, inquiry_id):
    """الرد على استعلام"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'طريقة غير مسموحة'})
    
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)
        inquiry = get_object_or_404(Inquiry, id=inquiry_id)
        
        form = InquiryResponseForm(request.POST)
        
        if form.is_valid():
            response_text = form.cleaned_data['response']
            
            # تحديث الاستعلام
            inquiry.response = response_text
            inquiry.is_resolved = True
            inquiry.responded_by = request.user
            inquiry.resolved_at = timezone.now()
            inquiry.save()
            
            logger.info(f'تم الرد على الاستعلام {inquiry.get_inquiry_id()} بواسطة {request.user.username} من IP: {get_client_ip(request)}')
            
            # إرسال البريد الإلكتروني للمتعامل
            email_result = email_service.send_inquiry_response(inquiry, response_text)
            
            if email_result['success']:
                logger.info(f'تم إرسال بريد إلكتروني للاستعلام {inquiry.get_inquiry_id()}')
                response_message = 'تم إرسال الرد بنجاح وتم إبلاغ المتعامل عبر البريد الإلكتروني'
            else:
                logger.warning(f'فشل إرسال البريد الإلكتروني للاستعلام {inquiry.get_inquiry_id()}: {email_result.get("message")}')
                response_message = f'تم إرسال الرد بنجاح ولكن فشل إرسال البريد الإلكتروني: {email_result.get("message")}'
            
            return JsonResponse({
                'success': True, 
                'message': response_message,
                'inquiry_id': inquiry.get_inquiry_id(),
                'email_sent': email_result['success']
            })
        else:
            # إرجاع أول خطأ في النموذج
            first_error = next(iter(form.errors.values()))[0]
            return JsonResponse({'success': False, 'message': first_error})
        
    except EmployeeProfile.DoesNotExist:
        logger.error(f'محاولة الرد بدون ملف موظف: {request.user.username} من IP: {get_client_ip(request)}')
        return JsonResponse({'success': False, 'message': 'خطأ في الوصول للبيانات'})
