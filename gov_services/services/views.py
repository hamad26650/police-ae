from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import Service, SiteSettings, ServiceRequest, EmployeeProfile, Center, SMSMessage, Inquiry
from .forms import InquiryForm, StaffLoginForm, InquiryResponseForm, ServiceRequestForm
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

@rate_limit(key_prefix='submit_report', limit=5, period=3600)  # 5 طلبات في الساعة
def submit_report(request):
    """صفحة تقديم البلاغ/الطلب الإلكتروني"""
    form = ServiceRequestForm()
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        
        if form.is_valid():
            try:
                # اختيار مركز افتراضي
                default_center = Center.objects.first()
                
                if not default_center:
                    messages.error(request, 'عذراً، لا توجد مراكز متاحة حالياً. يرجى المحاولة لاحقاً.')
                    return redirect('services:submit_report')
                
                # إنشاء طلب خدمة جديد
                service_request = ServiceRequest.objects.create(
                    service=Service.objects.first() or Service.objects.create(
                        name='sharjah_police',
                        slug='sharjah-police',
                        description='خدمات شرطة الشارقة',
                        is_active=True
                    ),
                    center=default_center,
                    requester_name=form.cleaned_data['requester_name'],
                    requester_email=form.cleaned_data['requester_email'],
                    requester_phone=form.cleaned_data['requester_phone'],
                    requester_national_id=form.cleaned_data['requester_national_id'],
                    request_details=form.cleaned_data['request_details'],
                    status='pending',
                    priority='medium'
                )
                
                # تسجيل في الـ logs
                logger.info(f'طلب جديد: {service_request.get_request_id()} من {service_request.requester_name}')
                
                # رسالة نجاح
                messages.success(
                    request, 
                    f'تم تقديم طلبك بنجاح! رقم الطلب: {service_request.get_request_id()}. '
                    f'سيتم التواصل معك عبر البريد الإلكتروني: {service_request.requester_email}'
                )
                
                # إرسال إيميل (إذا كان مفعّل)
                try:
                    email_service.send_request_confirmation(service_request)
                except Exception as e:
                    logger.warning(f'فشل إرسال الإيميل: {str(e)}')
                
                return redirect('services:submit_report')
                
            except Exception as e:
                logger.error(f'خطأ في إنشاء الطلب: {str(e)}')
                messages.error(request, 'عذراً، حدث خطأ أثناء تقديم الطلب. يرجى المحاولة لاحقاً.')
        else:
            # عرض أخطاء النموذج
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    
    context = {'form': form}
    return render(request, 'services/submit_report.html', context)

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
            
            # إرسال إيميل تأكيد للمواطن
            try:
                email_service.send_inquiry_confirmation(inquiry)
                logger.info(f'تم إرسال إيميل تأكيد للاستعلام {inquiry.get_inquiry_id()}')
            except Exception as e:
                logger.warning(f'فشل إرسال إيميل تأكيد: {str(e)}')
            
            # إرسال إشعار للموظفين
            try:
                email_service.notify_staff_new_inquiry(inquiry)
                logger.info(f'تم إرسال إشعار للموظفين عن الاستعلام {inquiry.get_inquiry_id()}')
            except Exception as e:
                logger.warning(f'فشل إرسال إشعار للموظفين: {str(e)}')
            
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

def staff_login(request):
    """صفحة تسجيل دخول الموظفين - مبسطة"""
    # إذا مسجل دخول، روح Dashboard مباشرة
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('services:staff_dashboard')
    
    form = StaffLoginForm()
    
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # التحقق البسيط: is_staff أو is_superuser
                if user.is_staff or user.is_superuser:
                    # تسجيل الدخول مباشرة
                    login(request, user)
                    messages.success(request, f'مرحباً {user.get_full_name() or user.username}!')
                    return redirect('services:staff_dashboard')
                else:
                    messages.error(request, 'غير مخول للوصول')
            else:
                # اسم المستخدم أو كلمة المرور خاطئة
                logger.warning(f'محاولة دخول فاشلة: {username} من IP: {get_client_ip(request)}')
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
        else:
            # عرض أخطاء النموذج
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    
    context = {'form': form}
    return render(request, 'services/staff_login.html', context)

def staff_logout(request):
    """تسجيل خروج الموظفين"""
    if 'welcomed' in request.session:
        del request.session['welcomed']
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('services:staff_login')

def staff_dashboard(request):
    """لوحة تحكم الموظفين - آمن ومحمي من الأخطاء"""
    # تحقق: لازم يكون مسجل دخول
    if not request.user.is_authenticated:
        return redirect('services:staff_login')
    
    # تحقق: لازم يكون staff أو admin
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول')
        return redirect('services:staff_login')
    
    try:
        # جيب أو أنشئ المركز بشكل آمن
        center = Center.objects.first()
        if not center:
            center = Center.objects.create(
                name='مركز شرطة البحيرة',
                location='الشارقة',
                is_active=True
            )
        
        # جيب أو أنشئ ملف الموظف بشكل آمن
        employee_profile, created = EmployeeProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'employee_id': f'EMP-{request.user.id}',
                'department': 'قسم عام',
                'role': 'admin' if request.user.is_superuser else 'center',
                'center': center,
                'phone': '123456',
                'is_active': True
            }
        )
    except Exception as e:
        # لو صار أي خطأ، اعرض رسالة واضحة
        messages.error(request, f'حدث خطأ: {str(e)}')
        return redirect('services:staff_login')
    
    # جلب الاستعلامات عن البلاغات (جميع الموظفين يرون جميع الاستعلامات)
    inquiries = Inquiry.objects.filter(inquiry_type='report_status').order_by('-created_at')
    
    # فلترة حسب الحالة إذا تم تحديدها
    status_filter = request.GET.get('status')
    if status_filter == 'resolved':
        inquiries = inquiries.filter(status='resolved')
    elif status_filter == 'pending':
        inquiries = inquiries.filter(status='pending')
    elif status_filter == 'rejected':
        inquiries = inquiries.filter(status='rejected')
    
    # البحث عن طريق رقم المرجع فقط (مطابقة تامة)
    search_query = request.GET.get('search')
    if search_query:
        inquiries = inquiries.filter(id__exact=search_query.strip())
    
    # إحصائيات
    all_inquiries = Inquiry.objects.filter(inquiry_type='report_status')
    total_inquiries = all_inquiries.count()
    pending_inquiries = all_inquiries.filter(status='pending').count()
    resolved_inquiries = all_inquiries.filter(status='resolved').count()
    rejected_inquiries = all_inquiries.filter(status='rejected').count()
    
    context = {
        'employee_profile': employee_profile,
        'inquiries': inquiries,
        'current_status': status_filter,
        'search_query': search_query,
        'total_inquiries': total_inquiries,
        'pending_inquiries': pending_inquiries,
        'resolved_inquiries': resolved_inquiries,
        'rejected_inquiries': rejected_inquiries,
        'current_user': request.user,  # للتحقق من حجز الطلبات
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
            
            # إرسال البريد الإلكتروني مباشرة (بدون threading لضمان الإرسال)
            from django.conf import settings
            
            try:
                # التحقق من الإعدادات
                if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    # محاولة الإرسال مباشرة
                    logger.info(f'📧 بدء إرسال بريد إلكتروني للاستعلام {inquiry.get_inquiry_id()}')
                    
                    # تعيين timeout
                    import socket
                    old_timeout = socket.getdefaulttimeout()
                    socket.setdefaulttimeout(15)  # 15 ثانية
                    
                    try:
                        email_result = email_service.send_inquiry_response(inquiry, response_text)
                        
                        if email_result['success']:
                            logger.info(f'✅ نجح إرسال البريد للاستعلام {inquiry.get_inquiry_id()} إلى {inquiry.phone}')
                        else:
                            logger.warning(f'⚠️ فشل إرسال البريد: {email_result.get("message", "غير محدد")}')
                    finally:
                        # إعادة timeout
                        socket.setdefaulttimeout(old_timeout)
                else:
                    logger.warning(f'⚠️ إعدادات البريد غير متوفرة للاستعلام {inquiry.get_inquiry_id()}')
                    
            except Exception as e:
                error_type = type(e).__name__
                logger.error(f'❌ خطأ في إرسال البريد للاستعلام {inquiry.get_inquiry_id()}: {error_type} - {str(e)[:200]}')
            
            # الرد فوراً للموظف (بدون انتظار الإيميل)
            return JsonResponse({
                'success': True, 
                'message': 'تم حفظ الرد بنجاح وسيتم إرسال البريد الإلكتروني',
                'inquiry_id': inquiry.get_inquiry_id(),
                'email_sent': True  # سيُرسل في الخلفية
            })
        else:
            # إرجاع أول خطأ في النموذج
            first_error = next(iter(form.errors.values()))[0]
            return JsonResponse({'success': False, 'message': first_error})
        
    except EmployeeProfile.DoesNotExist:
        logger.error(f'محاولة الرد بدون ملف موظف: {request.user.username} من IP: {get_client_ip(request)}')
        return JsonResponse({'success': False, 'message': 'خطأ في الوصول للبيانات'})


# ===================== نظام حجز الطلبات =====================

@login_required(login_url='services:staff_login')
def reserve_inquiry(request, inquiry_id):
    """حجز طلب للموظف"""
    if request.method == 'POST':
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id, inquiry_type='report_status')
            
            # التحقق من أن الطلب غير محجوز
            if inquiry.reserved_by:
                return JsonResponse({
                    'success': False,
                    'message': f'هذا الطلب محجوز بالفعل من قبل {inquiry.reserved_by.get_full_name() or inquiry.reserved_by.username}'
                })
            
            # حجز الطلب
            inquiry.reserved_by = request.user
            inquiry.reserved_at = timezone.now()
            inquiry.save()
            
            logger.info(f'حجز طلب #{inquiry.id} بواسطة {request.user.username}')
            
            return JsonResponse({
                'success': True,
                'message': 'تم حجز الطلب بنجاح'
            })
            
        except Inquiry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'الطلب غير موجود'})
        except Exception as e:
            logger.error(f'خطأ في حجز الطلب: {str(e)}')
            return JsonResponse({'success': False, 'message': 'حدث خطأ أثناء حجز الطلب'})
    
    return JsonResponse({'success': False, 'message': 'طريقة غير صحيحة'})


@login_required(login_url='services:staff_login')
def unreserve_inquiry(request, inquiry_id):
    """فك حجز طلب"""
    if request.method == 'POST':
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id, inquiry_type='report_status')
            
            # التحقق من أن الطلب محجوز من قبل الموظف الحالي أو أنه مدير
            if inquiry.reserved_by != request.user and not request.user.is_superuser:
                return JsonResponse({
                    'success': False,
                    'message': 'لا يمكنك فك حجز طلب محجوز من قبل موظف آخر'
                })
            
            # فك الحجز
            inquiry.reserved_by = None
            inquiry.reserved_at = None
            inquiry.save()
            
            logger.info(f'فك حجز طلب #{inquiry.id} بواسطة {request.user.username}')
            
            return JsonResponse({
                'success': True,
                'message': 'تم فك حجز الطلب بنجاح'
            })
            
        except Inquiry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'الطلب غير موجود'})
        except Exception as e:
            logger.error(f'خطأ في فك حجز الطلب: {str(e)}')
            return JsonResponse({'success': False, 'message': 'حدث خطأ أثناء فك حجز الطلب'})
    
    return JsonResponse({'success': False, 'message': 'طريقة غير صحيحة'})


@login_required(login_url='services:staff_login')
def reject_inquiry(request, inquiry_id):
    """رفض طلب"""
    if request.method == 'POST':
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id, inquiry_type='report_status')
            rejection_reason = request.POST.get('rejection_reason', '').strip()
            
            if not rejection_reason:
                return JsonResponse({'success': False, 'message': 'يرجى كتابة سبب الرفض'})
            
            # التحقق من أن الطلب محجوز من قبل الموظف الحالي
            if inquiry.reserved_by != request.user and not request.user.is_superuser:
                return JsonResponse({
                    'success': False,
                    'message': 'يجب حجز الطلب أولاً قبل رفضه'
                })
            
            # رفض الطلب
            inquiry.status = 'rejected'
            inquiry.rejection_reason = rejection_reason
            inquiry.response = f"تم رفض الطلب. السبب: {rejection_reason}"
            inquiry.is_resolved = True
            inquiry.responded_by = request.user
            inquiry.resolved_at = timezone.now()
            inquiry.save()
            
            logger.info(f'رفض طلب #{inquiry.id} بواسطة {request.user.username}')
            
            return JsonResponse({
                'success': True,
                'message': 'تم رفض الطلب بنجاح'
            })
            
        except Inquiry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'الطلب غير موجود'})
        except Exception as e:
            logger.error(f'خطأ في رفض الطلب: {str(e)}')
            return JsonResponse({'success': False, 'message': 'حدث خطأ أثناء رفض الطلب'})
    
    return JsonResponse({'success': False, 'message': 'طريقة غير صحيحة'})


@login_required(login_url='services:staff_login')
def respond_inquiry(request, inquiry_id):
    """الرد على طلب"""
    if request.method == 'POST':
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id, inquiry_type='report_status')
            response_text = request.POST.get('response_text', '').strip()
            
            if not response_text:
                return JsonResponse({'success': False, 'message': 'يرجى كتابة الرد'})
            
            # التحقق من أن الطلب محجوز من قبل الموظف الحالي
            if inquiry.reserved_by != request.user and not request.user.is_superuser:
                return JsonResponse({
                    'success': False,
                    'message': 'يجب حجز الطلب أولاً قبل الرد عليه'
                })
            
            # الرد على الطلب
            inquiry.status = 'resolved'
            inquiry.response = response_text
            inquiry.is_resolved = True
            inquiry.responded_by = request.user
            inquiry.resolved_at = timezone.now()
            inquiry.save()
            
            logger.info(f'تم الرد على طلب #{inquiry.id} بواسطة {request.user.username}')
            
            return JsonResponse({
                'success': True,
                'message': 'تم الرد على الطلب بنجاح'
            })
            
        except Inquiry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'الطلب غير موجود'})
        except Exception as e:
            logger.error(f'خطأ في الرد على الطلب: {str(e)}')
            return JsonResponse({'success': False, 'message': 'حدث خطأ أثناء الرد على الطلب'})
    
    return JsonResponse({'success': False, 'message': 'طريقة غير صحيحة'})
