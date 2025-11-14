from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'services'

def redirect_to_home(request):
    return redirect('services:home')

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test_page, name='test'),  # صفحة اختبار جديدة
    
    # النيابة العامة
    path('prosecution/', views.prosecution, name='prosecution'),
    path('petition-number/', views.petition_number, name='petition_number'),
    path('submit-petition/', views.submit_petition, name='submit_petition'),
    
    # الهوية الرقمية
    path('digital-identity/', views.digital_identity, name='digital_identity'),
    path('digital_identity/', views.digital_identity, name='digital_identity_alt'),  # مسار بديل
    
    # وزارة الداخلية
    path('interior-ministry/', views.interior_ministry, name='interior_ministry'),
    path('interior_ministry/', views.interior_ministry, name='interior_ministry_alt'),  # مسار بديل
    path('interior-ministry/bank-contact/', views.bank_contact, name='bank_contact'),
    path('submit-report/', views.submit_report, name='submit_report'),
    path('check-report-status/', views.check_report_status, name='check_report_status'),
    
    # نموذج 1
    path('model1/', views.model1, name='model1'),
    
    # فتح بلاغ جنائي
    path('criminal-report/', views.criminal_report, name='criminal_report'),
    
    # نظام الموظفين
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/home/', views.staff_home, name='staff_home'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/report-completion/', views.staff_report_completion, name='staff_report_completion'),
    path('staff/report-inquiry/', views.staff_report_inquiry, name='staff_report_inquiry'),
    path('staff/criminal-reports/', views.staff_criminal_reports, name='staff_criminal_reports'),
    path('staff/criminal-report-detail/<int:report_id>/', views.criminal_report_detail, name='criminal_report_detail'),
    path('staff/criminal-report/<int:report_id>/', views.get_report_details, name='get_report_details'),
    path('staff/criminal-report/<int:report_id>/reserve/', views.reserve_criminal_report, name='reserve_criminal_report'),
    path('staff/criminal-report/<int:report_id>/release/', views.release_criminal_report, name='release_criminal_report'),
    path('staff/criminal-report/<int:report_id>/status/', views.update_report_status, name='update_report_status'),
    path('staff/criminal-report/<int:report_id>/notes/', views.save_report_notes, name='save_report_notes'),
    path('staff/note/<int:note_id>/delete/', views.delete_report_note, name='delete_report_note'),
    path('staff/create-official-report/<int:report_id>/', views.create_official_report, name='create_official_report'),
    path('staff/update-request/<int:request_id>/', views.update_request_status, name='update_request_status'),
    
    # نظام الحجز والإجراءات
    path('staff/reserve-request/<int:request_id>/', views.reserve_request, name='reserve_request'),
    path('staff/release-request/<int:request_id>/', views.release_request, name='release_request'),
    path('staff/send-sms/<int:request_id>/', views.send_sms, name='send_sms'),
    path('staff/reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    
    # نظام الاستعلامات والرد
    path('staff/respond-inquiry/<int:inquiry_id>/', views.respond_inquiry, name='respond_inquiry'),
    
    # نظام حجز الطلبات
    path('staff/reserve-inquiry/<int:inquiry_id>/', views.reserve_inquiry, name='reserve_inquiry'),
    path('staff/unreserve-inquiry/<int:inquiry_id>/', views.unreserve_inquiry, name='unreserve_inquiry'),
    path('staff/reject-inquiry/<int:inquiry_id>/', views.reject_inquiry, name='reject_inquiry'),
    
    # روابط وهمية للصفحات غير المتاحة
    path('inquiry/', redirect_to_home, name='inquiry'),
    path('about/', redirect_to_home, name='about'),
    path('contact/', redirect_to_home, name='contact'),
    
    # إعادة توجيه للمسارات الخاطئة الشائعة
    path('home_page/index.html', redirect_to_home, name='home_page_redirect'),
]