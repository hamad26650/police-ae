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
    path('submit-report/', views.submit_report, name='submit_report'),
    path('check-report-status/', views.check_report_status, name='check_report_status'),
    
    # نموذج 1
    path('model1/', views.model1, name='model1'),
    
    # نظام الموظفين
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/update-request/<int:request_id>/', views.update_request_status, name='update_request_status'),
    
    # نظام الحجز والإجراءات
    path('staff/reserve-request/<int:request_id>/', views.reserve_request, name='reserve_request'),
    path('staff/release-request/<int:request_id>/', views.release_request, name='release_request'),
    path('staff/send-sms/<int:request_id>/', views.send_sms, name='send_sms'),
    path('staff/reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    
    # نظام الاستعلامات
    path('staff/respond-inquiry/<int:inquiry_id>/', views.respond_to_inquiry, name='respond_to_inquiry'),
    
    # روابط وهمية للصفحات غير المتاحة
    path('inquiry/', redirect_to_home, name='inquiry'),
    path('about/', redirect_to_home, name='about'),
    path('contact/', redirect_to_home, name='contact'),
    
    # إعادة توجيه للمسارات الخاطئة الشائعة
    path('home_page/index.html', redirect_to_home, name='home_page_redirect'),
]