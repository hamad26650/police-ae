from django.contrib import admin
from django.contrib.admin import AdminSite

# تخصيص عنوان لوحة الإدارة
admin.site.site_header = "🚓 إدارة نظام شرطة الشارقة"
admin.site.site_title = "لوحة التحكم | شرطة الشارقة"
admin.site.index_title = "مرحباً في لوحة التحكم الرئيسية"

# إضافة CSS مخصص
class CustomAdminSite(AdminSite):
    class Media:
        css = {
            'all': ('services/admin/css/custom_admin.css',)
        }
from .models import Service, ServiceRequest, Inquiry, SiteSettings, Center, EmployeeProfile, SMSMessage, AuditLog

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['requester_name', 'service', 'status', 'center', 'assigned_to', 'reserved_by', 'created_at']
    list_filter = ['status', 'service', 'center', 'created_at']
    search_fields = ['requester_name', 'requester_email', 'requester_national_id']
    list_editable = ['status', 'center', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at', 'reserved_at']
    
    fieldsets = (
        ('معلومات المتقدم', {
            'fields': ('requester_name', 'requester_email', 'requester_phone', 'requester_national_id')
        }),
        ('تفاصيل الطلب', {
            'fields': ('service', 'request_details', 'status')
        }),
        ('إدارة الطلب', {
            'fields': ('center', 'assigned_to', 'notes')
        }),
        ('نظام الحجز', {
            'fields': ('reserved_by', 'reserved_at'),
            'classes': ('collapse',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'inquiry_type', 'is_resolved', 'responded_by', 'created_at']
    list_filter = ['inquiry_type', 'is_resolved', 'created_at']
    search_fields = ['full_name', 'email', 'request_reference']
    list_editable = ['is_resolved']
    readonly_fields = ['created_at', 'resolved_at']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone']
    
    def has_add_permission(self, request):
        # السماح بإنشاء إعداد واحد فقط
        return not SiteSettings.objects.exists()

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'location', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'location']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'role', 'center', 'department', 'is_active']
    list_filter = ['role', 'center', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    list_editable = ['role', 'center', 'is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('معلومات المستخدم', {
            'fields': ('user', 'employee_id')
        }),
        ('معلومات الوظيفة', {
            'fields': ('role', 'center', 'department')
        }),
        ('معلومات إضافية', {
            'fields': ('phone', 'is_active', 'created_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'center')
    
    def has_delete_permission(self, request, obj=None):
        # منع حذف الإعدادات
        return False

@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ['request', 'sender', 'phone_number', 'is_sent', 'sent_at']
    list_filter = ['is_sent', 'sent_at']
    search_fields = ['request__requester_name', 'phone_number', 'message']
    readonly_fields = ['sent_at']
    
    fieldsets = (
        ('معلومات الرسالة', {
            'fields': ('request', 'sender', 'message')
        }),
        ('معلومات الإرسال', {
            'fields': ('phone_number', 'is_sent', 'sent_at')
        }),
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'ip_address', 'description_short')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'user_agent', 'timestamp')
    ordering = ('-timestamp',)
    list_per_page = 50
    
    def description_short(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_short.short_description = 'الوصف'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
