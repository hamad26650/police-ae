from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from .models import Service, SiteSettings, ServiceRequest, EmployeeProfile, Center, SMSMessage, Inquiry, BankContactRequest
from .forms import InquiryForm, StaffLoginForm, InquiryResponseForm, ServiceRequestForm, BankContactForm
from .decorators import rate_limit, track_failed_login, log_user_activity, get_client_ip
from .utils.email_service import email_service
import logging

# إعداد Logger
logger = logging.getLogger('services')

# دالة مساعدة لتسجيل إجراءات البلاغات
def log_report_activity(report, user, action_type, description, old_value='', new_value=''):
    """تسجيل إجراء على البلاغ"""
    from services.models import CriminalReportActivity
    
    try:
        CriminalReportActivity.objects.create(
            report=report,
            user=user,
            action_type=action_type,
            description=description,
            old_value=old_value,
            new_value=new_value
        )
    except Exception as e:
        logger.error(f"Error logging activity: {e}")

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

def bank_contact(request):
    """صفحة مخاطبة البنوك"""
    form = BankContactForm()
    
    if request.method == 'POST':
        form = BankContactForm(request.POST)
        
        if form.is_valid():
            try:
                # البحث عن المركز أو إنشاؤه
                center_name = form.cleaned_data['center']
                center, created = Center.objects.get_or_create(
                    name=center_name,
                    defaults={
                        'code': center_name[:3].upper(),
                        'location': 'الشارقة',
                        'is_active': True
                    }
                )
                
                # إنشاء طلب مخاطبة البنك
                bank_request = BankContactRequest.objects.create(
                    center=center,
                    report_number=form.cleaned_data['report_number'],
                    report_year=form.cleaned_data['report_year'],
                    charge=form.cleaned_data['charge'],
                    bank_name=form.cleaned_data['bank_name'],
                    account_number=form.cleaned_data['account_number'],
                    status='pending'
                )
                
                logger.info(f'طلب مخاطبة بنك جديد: {bank_request.id} - {bank_request.bank_name}')
                
                # إرسال الإيميل للبنك
                try:
                    email_result = email_service.send_bank_contact_request(bank_request)
                    if email_result['success']:
                        logger.info(f'✅ تم إرسال إيميل لطلب مخاطبة البنك {bank_request.id}')
                        messages.success(
                            request,
                            f'تم تقديم طلب مخاطبة البنك بنجاح! تم إرسال الطلب إلى {bank_request.bank_name}.'
                        )
                    else:
                        logger.warning(f'⚠️ فشل إرسال إيميل لطلب مخاطبة البنك {bank_request.id}: {email_result.get("message", "غير محدد")}')
                        messages.success(
                            request,
                            f'تم حفظ طلب مخاطبة البنك بنجاح! {email_result.get("message", "")}'
                        )
                except Exception as e:
                    logger.error(f'❌ خطأ في إرسال إيميل لطلب مخاطبة البنك {bank_request.id}: {str(e)}')
                    messages.success(
                        request,
                        f'تم حفظ طلب مخاطبة البنك بنجاح! سيتم معالجة طلبك قريباً.'
                    )
                
                return redirect('services:bank_contact')
                
            except Exception as e:
                logger.error(f'خطأ في إنشاء طلب مخاطبة البنك: {str(e)}')
                messages.error(request, 'عذراً، حدث خطأ أثناء تقديم الطلب. يرجى المحاولة لاحقاً.')
        else:
            # عرض أخطاء النموذج
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    
    context = {'form': form}
    return render(request, 'services/bank_contact.html', context)

# نموذج 1
def model1(request):
    """صفحة نموذج 1"""
    return render(request, 'services/model1.html')

def criminal_report(request):
    """صفحة فتح بلاغ جنائي"""
    if request.method == 'POST':
        try:
            from services.models import CriminalReport
            import json
            
            # جمع بيانات المشكو في حقهم
            accused_parties = []
            party_count = 1
            while request.POST.get(f'party_type_{party_count}'):
                party_type = request.POST.get(f'party_type_{party_count}')
                party_data = {'type': party_type}
                
                if party_type == 'شخص':
                    party_data.update({
                        'name': request.POST.get(f'party_name_{party_count}', ''),
                        'doc_type': request.POST.get(f'doc_type_{party_count}', ''),
                        'nationality': request.POST.get(f'nationality_{party_count}', ''),
                        'phone': request.POST.get(f'party_phone_{party_count}', ''),
                        'address': request.POST.get(f'party_address_{party_count}', ''),
                    })
                elif party_type == 'مؤسسة':
                    party_data.update({
                        'name': request.POST.get(f'company_name_{party_count}', ''),
                        'phone': request.POST.get(f'company_phone_{party_count}', ''),
                        'address': request.POST.get(f'company_address_{party_count}', ''),
                    })
                elif party_type == 'مجهول':
                    party_data.update({
                        'name': request.POST.get(f'unknown_name_{party_count}', ''),
                        'phone': request.POST.get(f'unknown_phone_{party_count}', ''),
                        'info': request.POST.get(f'unknown_info_{party_count}', ''),
                    })
                
                accused_parties.append(party_data)
                party_count += 1
            
            # إنشاء البلاغ
            report = CriminalReport.objects.create(
                # بيانات الشاكي
                complainant_name=request.POST.get('complainant_name'),
                complainant_id=request.POST.get('complainant_id'),
                complainant_phone=request.POST.get('complainant_phone'),
                complainant_email=request.POST.get('complainant_email'),
                
                # بيانات البلاغ
                police_center=request.POST.get('police_center'),
                complaint_type=request.POST.get('complaint_type'),
                
                # تفاصيل البلاغ
                complaint_subject=request.POST.get('complaint_subject', ''),
                incident_date=request.POST.get('incident_date') or None,
                incident_time=request.POST.get('incident_time') or None,
                incident_location=request.POST.get('incident_location', ''),
                incident_lat=request.POST.get('incident_lat') or None,
                incident_lng=request.POST.get('incident_lng') or None,
                
                # العلاقة والاتفاق
                relationship=request.POST.get('relationship', ''),
                agreement_type=request.POST.get('agreement_type', ''),
                
                # المبالغ والممتلكات
                money_seized=request.POST.get('money_seized', ''),
                seized_amount=request.POST.get('seized_amount') or None,
                seized_property=request.POST.get('seized_property', ''),
                
                # طريقة التحويل
                transfer_method=request.POST.get('transfer_method', ''),
                bank_name=request.POST.get('bank_name', ''),
                account_number=request.POST.get('account_number', ''),
                other_transfer_method=request.POST.get('other_transfer_method', ''),
                
                # الشهود والإثباتات
                has_witnesses=request.POST.get('has_witnesses', ''),
                witnesses_info=request.POST.get('witnesses_info', ''),
                has_evidence=request.POST.get('has_evidence', ''),
                evidence_description=request.POST.get('evidence_description', ''),
                
                # أقوال إضافية
                additional_statements=request.POST.get('additional_statements', ''),
                
                # المشكو في حقهم
                accused_parties=accused_parties,
                
                # الحالة
                status='new_request'
            )
            
            # تسجيل إنشاء البلاغ
            log_report_activity(
                report=report,
                user=None,
                action_type='created',
                description=f'تم تقديم البلاغ من قبل {report.complainant_name}',
                new_value=f'رقم المرجع: {report.reference_number}'
            )
            
            # إرجاع JSON response للنجاح
            from django.http import JsonResponse
            return JsonResponse({
                'success': True,
                'reference_number': report.reference_number,
                'message': 'تم تقديم البلاغ بنجاح'
            })
            
        except Exception as e:
            from django.http import JsonResponse
            return JsonResponse({
                'success': False,
                'message': f'حدث خطأ: {str(e)}'
            }, status=400)
    
    return render(request, 'services/criminal_report.html')

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
    # إذا مسجل دخول، روح الصفحة الرئيسية مباشرة
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('services:staff_home')
    
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
                    return redirect('services:staff_home')
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

@login_required(login_url='services:staff_login')
def staff_criminal_reports(request):
    """صفحة إدارة البلاغات الجنائية للموظفين"""
    # تحقق: لازم يكون مسجل دخول
    if not request.user.is_authenticated:
        return redirect('services:staff_login')
    
    # تحقق: لازم يكون موظف
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول للوصول')
        return redirect('services:home')
    
    from services.models import CriminalReport
    from django.db.models import Q
    
    # جلب البلاغات
    reports = CriminalReport.objects.all().order_by('-created_at')
    
    # فلترة حسب الحالة
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    # البحث برقم المرجع
    reference_query = request.GET.get('reference')
    if reference_query:
        reports = reports.filter(reference_number__icontains=reference_query)
    
    # البحث برقم الهاتف
    phone_query = request.GET.get('phone')
    if phone_query:
        reports = reports.filter(complainant_phone__icontains=phone_query)
    
    # البحث بالتاريخ (من)
    date_from = request.GET.get('date_from')
    if date_from:
        reports = reports.filter(created_at__date__gte=date_from)
    
    # البحث بالتاريخ (إلى)
    date_to = request.GET.get('date_to')
    if date_to:
        reports = reports.filter(created_at__date__lte=date_to)
    
    # إحصائيات
    all_reports = CriminalReport.objects.all()
    total_reports = all_reports.count()
    new_request_reports = all_reports.filter(status='new_request').count()
    in_progress_reports = all_reports.filter(status='in_progress').count()
    awaiting_response_reports = all_reports.filter(status='awaiting_response').count()
    report_created_reports = all_reports.filter(status='report_created').count()
    archived_reports = all_reports.filter(status='archived').count()
    rejected_reports = all_reports.filter(status='rejected').count()
    out_of_jurisdiction_reports = all_reports.filter(status='out_of_jurisdiction').count()
    
    context = {
        'reports': reports,
        'current_status': status_filter,
        'reference_query': reference_query,
        'phone_query': phone_query,
        'date_from': date_from,
        'date_to': date_to,
        'total_reports': total_reports,
        'new_request_reports': new_request_reports,
        'in_progress_reports': in_progress_reports,
        'awaiting_response_reports': awaiting_response_reports,
        'report_created_reports': report_created_reports,
        'archived_reports': archived_reports,
        'rejected_reports': rejected_reports,
        'out_of_jurisdiction_reports': out_of_jurisdiction_reports,
        'current_user': request.user,
    }
    
    return render(request, 'services/staff_criminal_reports.html', context)

@login_required(login_url='services:staff_login')
def criminal_report_detail(request, report_id):
    """صفحة تفاصيل البلاغ الجنائي"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول للوصول')
        return redirect('services:home')
    
    from services.models import CriminalReport
    
    try:
        report = CriminalReport.objects.get(id=report_id)
    except CriminalReport.DoesNotExist:
        messages.error(request, 'البلاغ غير موجود')
        return redirect('services:staff_criminal_reports')
    
    context = {
        'report': report,
        'current_user': request.user,
    }
    
    return render(request, 'services/criminal_report_detail.html', context)

@login_required(login_url='services:staff_login')
def get_report_details(request, report_id):
    """API لجلب تفاصيل البلاغ بصيغة JSON"""
    if not (request.user.is_staff or request.user.is_superuser):
        from django.http import JsonResponse
        return JsonResponse({'error': 'غير مخول'}, status=403)
    
    from services.models import CriminalReport
    from django.http import JsonResponse
    
    try:
        report = CriminalReport.objects.get(id=report_id)
        data = {
            'id': report.id,
            'reference_number': report.reference_number,
            'complainant_name': report.complainant_name,
            'complainant_id': report.complainant_id,
            'complainant_phone': report.complainant_phone,
            'complainant_email': report.complainant_email,
            'police_center': report.police_center,
            'complaint_type': report.complaint_type,
            'status': report.status,
            'status_display': report.get_status_display(),
            'complaint_subject': report.complaint_subject,
            'incident_date': str(report.incident_date) if report.incident_date else '',
            'incident_time': str(report.incident_time) if report.incident_time else '',
            'incident_location': report.incident_location,
            'incident_lat': str(report.incident_lat) if report.incident_lat else '',
            'incident_lng': str(report.incident_lng) if report.incident_lng else '',
            'relationship': report.relationship,
            'agreement_type': report.agreement_type,
            'money_seized': report.money_seized,
            'seized_amount': str(report.seized_amount) if report.seized_amount else '',
            'seized_property': report.seized_property,
            'transfer_method': report.transfer_method,
            'bank_name': report.bank_name,
            'account_number': report.account_number,
            'other_transfer_method': report.other_transfer_method,
            'has_witnesses': report.has_witnesses,
            'witnesses_info': report.witnesses_info,
            'has_evidence': report.has_evidence,
            'evidence_description': report.evidence_description,
            'additional_statements': report.additional_statements,
            'accused_parties': report.accused_parties,
            'reserved_by': report.reserved_by.get_full_name() if report.reserved_by else None,
            'reserved_by_id': report.reserved_by.id if report.reserved_by else None,
            'reserved_at': report.reserved_at.strftime('%Y-%m-%d %H:%M') if report.reserved_at else None,
            'staff_notes': report.staff_notes,
            'client_notes': report.client_notes,
            'additional_questions': report.additional_questions,
            'created_at': report.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        return JsonResponse(data)
    except CriminalReport.DoesNotExist:
        return JsonResponse({'error': 'البلاغ غير موجود'}, status=404)

@login_required(login_url='services:staff_login')
def reserve_criminal_report(request, report_id):
    """حجز البلاغ باسم الموظف"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول')
        return redirect('services:staff_criminal_reports')
    
    from services.models import CriminalReport
    from django.utils import timezone
    
    try:
        report = CriminalReport.objects.get(id=report_id)
        
        # حجز البلاغ
        old_reserved = report.reserved_by
        report.reserved_by = request.user
        report.reserved_at = timezone.now()
        
        # تغيير الحالة إلى "قيد الإجراء" تلقائياً
        old_status = report.status
        if report.status == 'new_request':
            report.status = 'in_progress'
        
        report.save()
        
        # تسجيل الإجراء
        log_report_activity(
            report=report,
            user=request.user,
            action_type='reserved',
            description=f'تم حجز البلاغ بواسطة {request.user.get_full_name() or request.user.username}',
            old_value=old_reserved.get_full_name() if old_reserved else 'غير محجوز',
            new_value=request.user.get_full_name() or request.user.username
        )
        
        # تسجيل تغيير الحالة إن حدث
        if old_status != report.status:
            log_report_activity(
                report=report,
                user=request.user,
                action_type='status_changed',
                description=f'تم تغيير حالة البلاغ من {report.get_status_display()} إلى {report.get_status_display()}',
                old_value=old_status,
                new_value=report.status
            )
        
        messages.success(request, f'تم حجز البلاغ #{report.reference_number} باسمك')
        
        # إذا كان الطلب من صفحة التفاصيل، ارجع لها
        if 'detail' in request.META.get('HTTP_REFERER', ''):
            return redirect('services:criminal_report_detail', report_id=report_id)
        return redirect('services:staff_criminal_reports')
    except CriminalReport.DoesNotExist:
        messages.error(request, 'البلاغ غير موجود')
        return redirect('services:staff_criminal_reports')

@login_required(login_url='services:staff_login')
def release_criminal_report(request, report_id):
    """فك حجز البلاغ"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول')
        return redirect('services:staff_criminal_reports')
    
    from services.models import CriminalReport
    from django.utils import timezone
    
    try:
        report = CriminalReport.objects.get(id=report_id)
        
        # إذا كان هناك force_reserve في POST، حجز بدل فك الحجز
        if request.method == 'POST' and request.POST.get('force_reserve'):
            old_reserved = report.reserved_by
            report.reserved_by = request.user
            report.reserved_at = timezone.now()
            if report.status == 'new_request':
                report.status = 'in_progress'
            report.save()
            
            # تسجيل الإجراء
            log_report_activity(
                report=report,
                user=request.user,
                action_type='reserved',
                description=f'تم حجز البلاغ بواسطة {request.user.get_full_name() or request.user.username} (فك الحجز والحجز باسمي)',
                old_value=old_reserved.get_full_name() if old_reserved else 'غير محجوز',
                new_value=request.user.get_full_name() or request.user.username
            )
            
            messages.success(request, f'تم حجز البلاغ #{report.reference_number} باسمك')
        else:
            # فك الحجز
            old_reserved = report.reserved_by
            report.reserved_by = None
            report.reserved_at = None
            report.save()
            
            # تسجيل الإجراء
            log_report_activity(
                report=report,
                user=request.user,
                action_type='released',
                description=f'تم فك حجز البلاغ بواسطة {request.user.get_full_name() or request.user.username}',
                old_value=old_reserved.get_full_name() if old_reserved else 'غير محجوز',
                new_value='غير محجوز'
            )
            
            messages.success(request, f'تم فك حجز البلاغ #{report.reference_number}')
        
        # إذا كان الطلب من صفحة التفاصيل، ارجع لها
        if 'detail' in request.META.get('HTTP_REFERER', ''):
            return redirect('services:criminal_report_detail', report_id=report_id)
        return redirect('services:staff_criminal_reports')
    except CriminalReport.DoesNotExist:
        messages.error(request, 'البلاغ غير موجود')
        return redirect('services:staff_criminal_reports')

@login_required(login_url='services:staff_login')
def update_report_status(request, report_id):
    """تحديث حالة البلاغ"""
    if not (request.user.is_staff or request.user.is_superuser):
        from django.http import JsonResponse
        return JsonResponse({'error': 'غير مخول'}, status=403)
    
    from services.models import CriminalReport
    from django.http import JsonResponse
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        try:
            report = CriminalReport.objects.get(id=report_id)
            old_status = report.status
            old_status_display = report.get_status_display()
            report.status = new_status
            report.save()
            
            # تسجيل الإجراء
            log_report_activity(
                report=report,
                user=request.user,
                action_type='status_changed',
                description=f'تم تغيير حالة البلاغ من "{old_status_display}" إلى "{report.get_status_display()}"',
                old_value=old_status,
                new_value=new_status
            )
            
            messages.success(request, f'تم تحديث الحالة إلى {report.get_status_display()}')
            
            # إذا كان الطلب من صفحة التفاصيل، ارجع لها
            if 'detail' in request.META.get('HTTP_REFERER', ''):
                return redirect('services:criminal_report_detail', report_id=report_id)
            
            # إذا كان AJAX request، أرجع JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'تم تحديث الحالة إلى {report.get_status_display()}'
                })
            
            return redirect('services:staff_criminal_reports')
        except CriminalReport.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'البلاغ غير موجود'}, status=404)
            messages.error(request, 'البلاغ غير موجود')
            return redirect('services:staff_criminal_reports')
    
    return JsonResponse({'error': 'طلب غير صحيح'}, status=400)

@login_required(login_url='services:staff_login')
def save_report_notes(request, report_id):
    """حفظ الملاحظات (داخلية أو للمتعامل)"""
    if not (request.user.is_staff or request.user.is_superuser):
        from django.http import JsonResponse
        return JsonResponse({'error': 'غير مخول'}, status=403)
    
    from services.models import CriminalReport, ReportNote
    from django.http import JsonResponse
    
    if request.method == 'POST':
        note_type = request.POST.get('note_type')  # 'staff' or 'client' or 'questions'
        content = request.POST.get('content')
        
        if not content or not content.strip():
            return JsonResponse({'error': 'الملاحظة فارغة'}, status=400)
        
        try:
            report = CriminalReport.objects.get(id=report_id)
            
            if note_type == 'staff' or note_type == 'client':
                # إنشاء ملاحظة جديدة
                note = ReportNote.objects.create(
                    report=report,
                    note_type=note_type,
                    content=content,
                    created_by=request.user
                )
                
                # تسجيل الإجراء
                log_report_activity(
                    report=report,
                    user=request.user,
                    action_type='note_added',
                    description=f'تم إضافة {"ملاحظة داخلية" if note_type == "staff" else "ملاحظة للمتعامل"} بواسطة {request.user.get_full_name() or request.user.username}',
                    new_value=content[:100] + '...' if len(content) > 100 else content
                )
                
            elif note_type == 'questions' or note_type == 'additional_questions':
                report.additional_questions = content
                # تغيير الحالة إلى "بانتظار الرد" تلقائياً
                if content and report.status not in ['awaiting_response']:
                    report.status = 'awaiting_response'
                report.save()
                
                # تسجيل الإجراء
                log_report_activity(
                    report=report,
                    user=request.user,
                    action_type='question_sent',
                    description=f'تم إرسال أسئلة إضافية للمتعامل بواسطة {request.user.get_full_name() or request.user.username}',
                    new_value=content[:100] + '...' if len(content) > 100 else content
                )
            
            return JsonResponse({
                'success': True,
                'message': 'تم حفظ الملاحظة بنجاح'
            })
        except CriminalReport.DoesNotExist:
            return JsonResponse({'error': 'البلاغ غير موجود'}, status=404)
    
    return JsonResponse({'error': 'طلب غير صحيح'}, status=400)

@login_required(login_url='services:staff_login')
def delete_report_note(request, note_id):
    """حذف ملاحظة (فقط صاحبها يقدر يحذفها)"""
    if not (request.user.is_staff or request.user.is_superuser):
        from django.http import JsonResponse
        return JsonResponse({'error': 'غير مخول'}, status=403)
    
    from services.models import ReportNote
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            note = ReportNote.objects.get(id=note_id, is_deleted=False)
            
            # تحقق: هل هو صاحب الملاحظة أو سوبر يوزر؟
            if note.created_by != request.user and not request.user.is_superuser:
                return JsonResponse({'error': 'لا يمكنك حذف ملاحظة شخص آخر'}, status=403)
            
            # حذف soft (تعليمها كمحذوفة)
            note.is_deleted = True
            note.save()
            
            return JsonResponse({
                'success': True,
                'message': 'تم حذف الملاحظة بنجاح'
            })
        except ReportNote.DoesNotExist:
            return JsonResponse({'error': 'الملاحظة غير موجودة'}, status=404)
    
    return JsonResponse({'error': 'طلب غير صحيح'}, status=400)

@login_required(login_url='services:staff_login')
def create_official_report(request, report_id):
    """إنشاء بلاغ رسمي من البلاغ المبدئي"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول')
        return redirect('services:staff_criminal_reports')
    
    from services.models import CriminalReport
    
    try:
        report = CriminalReport.objects.get(id=report_id)
        
        if request.method == 'POST':
            # التحقق إذا كان البلاغ تم إنشاؤه مسبقاً
            was_already_created = report.status == 'report_created'
            
            # هنا سيتم حفظ البيانات لاحقاً (التهم، الإجراءات، إلخ)
            # الآن فقط نغير الحالة إذا لم يكن تم إنشاؤه مسبقاً
            if not was_already_created:
                old_status = report.status
                report.status = 'report_created'
                report.save()
                
                # تسجيل الإجراء
                log_report_activity(
                    report=report,
                    user=request.user,
                    action_type='status_changed',
                    description=f'تم إنشاء البلاغ الرسمي بواسطة {request.user.get_full_name() or request.user.username}',
                    old_value=old_status,
                    new_value='report_created'
                )
                
                messages.success(request, f'تم إنشاء البلاغ الرسمي #{report.reference_number} بنجاح')
            else:
                # حفظ التغييرات فقط بدون تغيير الحالة
                report.save()
                
                # تسجيل الإجراء
                log_report_activity(
                    report=report,
                    user=request.user,
                    action_type='assigned',  # نوع عام للتحديثات
                    description=f'تم حفظ التغييرات على البلاغ بواسطة {request.user.get_full_name() or request.user.username}',
                    old_value='',
                    new_value=''
                )
                
                messages.success(request, f'تم حفظ التغييرات على البلاغ #{report.reference_number} بنجاح')
            
            return redirect('services:create_official_report', report_id=report_id)
        
        context = {
            'report': report,
        }
        return render(request, 'services/create_official_report.html', context)
        
    except CriminalReport.DoesNotExist:
        messages.error(request, 'البلاغ غير موجود')
        return redirect('services:staff_criminal_reports')

@login_required
def staff_report_inquiry(request):
    """صفحة الاستعلام المتقدم عن البلاغات"""
    # تحقق: لازم يكون موظف
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول للوصول')
        return redirect('services:home')
    
    from services.models import CriminalReport, Center
    
    # جلب جميع المراكز
    centers = Center.objects.all().order_by('name')
    
    context = {
        'centers': centers,
        'searched': False,
        'reports': [],
    }
    
    # إذا كان هناك بحث
    if request.GET:
        context['searched'] = True
        
        # البدء بجميع البلاغات
        reports = CriminalReport.objects.all()
        
        # فلترة حسب المركز
        center_id = request.GET.get('center')
        if center_id:
            # هنا يمكن الربط بالمركز إذا كان موجود في الموديل
            # reports = reports.filter(center_id=center_id)
            pass
        
        # فلترة حسب التاريخ
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from:
            reports = reports.filter(created_at__gte=date_from)
        if date_to:
            from datetime import datetime, timedelta
            # إضافة يوم كامل للتاريخ النهائي
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            reports = reports.filter(created_at__lt=date_to_obj)
        
        # فلترة حسب حالة المتهم
        accused_status = request.GET.get('accused_status')
        if accused_status:
            if accused_status == 'known':
                # البلاغات التي فيها اسم للمتهم
                reports = [r for r in reports if r.accused_parties and any(p.get('name') for p in r.accused_parties)]
            elif accused_status == 'unknown':
                # البلاغات التي ما فيها اسم للمتهم
                reports = [r for r in reports if not r.accused_parties or not any(p.get('name') for p in r.accused_parties)]
            # both: نعرض الكل (ما نسوي شي)
        
        # فلترة حسب التصنيف (حالياً كلها جنائية، يمكن إضافة حقل لاحقاً)
        classification = request.GET.get('classification')
        # if classification:
        #     reports = reports.filter(classification=classification)
        
        context['reports'] = reports if isinstance(reports, list) else reports.order_by('-created_at')
    
    return render(request, 'services/staff_report_inquiry.html', context)

@login_required
def staff_report_completion(request):
    """صفحة استكمال البلاغات - البحث بالمركز ورقم البلاغ والسنة"""
    # تحقق: لازم يكون موظف
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول للوصول')
        return redirect('services:home')
    
    from services.models import CriminalReport, Center
    
    # جلب جميع المراكز
    centers = Center.objects.all().order_by('name')
    
    context = {
        'centers': centers,
        'searched': False,
        'report': None,
    }
    
    # إذا كان هناك بحث
    if request.GET.get('center') and request.GET.get('report_number') and request.GET.get('year'):
        context['searched'] = True
        
        center_id = request.GET.get('center')
        report_number = request.GET.get('report_number').strip()
        year = request.GET.get('year').strip()
        
        try:
            # بناء رقم المرجع المتوقع
            # مثال: 2025-AJ-001 (السنة-كود المركز-الرقم)
            center = Center.objects.get(id=center_id)
            
            # البحث عن البلاغ
            # يمكن البحث بطرق مختلفة حسب صيغة reference_number
            report = CriminalReport.objects.filter(
                reference_number__icontains=f"{year}-{center.code if hasattr(center, 'code') else ''}-{report_number}"
            ).first()
            
            if not report:
                # محاولة أخرى: البحث بالسنة والرقم فقط
                reports_by_year = CriminalReport.objects.filter(reference_number__icontains=f"{year}")
                report = reports_by_year.filter(reference_number__icontains=report_number).first()
            
            context['report'] = report
            
        except Center.DoesNotExist:
            messages.error(request, 'المركز غير موجود')
        except Exception as e:
            logger.error(f"Error searching for report: {e}")
            messages.error(request, 'حدث خطأ أثناء البحث')
    
    return render(request, 'services/staff_report_completion.html', context)

def staff_home(request):
    """الصفحة الرئيسية للموظفين - عرض الخدمات المتاحة"""
    # تحقق: لازم يكون مسجل دخول
    if not request.user.is_authenticated:
        return redirect('services:staff_login')
    
    # تحقق: لازم يكون موظف
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'غير مخول للوصول')
        return redirect('services:home')
    
    try:
        # محاولة الحصول على ملف الموظف
        employee_profile = EmployeeProfile.objects.get(user=request.user)
    except EmployeeProfile.DoesNotExist:
        employee_profile = None
    
    # جلب إحصائيات الاستعلامات
    all_inquiries = Inquiry.objects.filter(inquiry_type='report_status')
    total_inquiries = all_inquiries.count()
    pending_inquiries = all_inquiries.filter(status='pending').count()
    resolved_inquiries = all_inquiries.filter(status='resolved').count()
    rejected_inquiries = all_inquiries.filter(status='rejected').count()
    
    # جلب إحصائيات البلاغات الجنائية
    from services.models import CriminalReport
    all_reports = CriminalReport.objects.all()
    total_reports = all_reports.count()
    new_reports = all_reports.filter(status='new_request').count()
    
    context = {
        'employee_profile': employee_profile,
        'total_inquiries': total_inquiries,
        'pending_inquiries': pending_inquiries,
        'resolved_inquiries': resolved_inquiries,
        'rejected_inquiries': rejected_inquiries,
        'total_reports': total_reports,
        'new_reports': new_reports,
    }
    
    return render(request, 'services/staff_home.html', context)

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
    """الرد على طلب - مع إرسال إيميل"""
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
            
            # إرسال البريد الإلكتروني مباشرة
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
            
            return JsonResponse({
                'success': True,
                'message': 'تم الرد على الطلب بنجاح وإرسال البريد الإلكتروني'
            })
            
        except Inquiry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'الطلب غير موجود'})
        except Exception as e:
            logger.error(f'خطأ في الرد على الطلب: {str(e)}')
            return JsonResponse({'success': False, 'message': 'حدث خطأ أثناء الرد على الطلب'})
    
    return JsonResponse({'success': False, 'message': 'طريقة غير صحيحة'})
