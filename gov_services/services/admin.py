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
from .models import Service, ServiceRequest, Inquiry, SiteSettings, Center, EmployeeProfile, SMSMessage, AuditLog, RequestAttachment, CriminalReport, CriminalReportActivity, ReportNote, BankContactRequest

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['requester_name', 'service', 'case_type', 'status', 'center', 'assigned_to', 'created_at']
    list_filter = ['status', 'case_type', 'service', 'center', 'created_at', 'manual_classification']
    search_fields = ['requester_name', 'requester_email', 'requester_national_id', 'petition_text']
    list_editable = ['status', 'center', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at', 'reserved_at', 'case_type_confidence', 'ai_analysis_notes']
    
    fieldsets = (
        ('معلومات المتقدم', {
            'fields': ('requester_name', 'requester_email', 'requester_phone', 'requester_national_id')
        }),
        ('تفاصيل الطلب', {
            'fields': ('service', 'request_details', 'petition_text', 'status')
        }),
        ('التصنيف الذكي', {
            'fields': ('case_type', 'case_type_confidence', 'manual_classification', 'ai_analysis_notes'),
            'classes': ('wide',)
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

@admin.register(RequestAttachment)
class RequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'request', 'file_type', 'get_file_size_display', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file_name', 'request__requester_name', 'extracted_text']
    readonly_fields = ['uploaded_at', 'extracted_text']
    
    fieldsets = (
        ('معلومات الملف', {
            'fields': ('request', 'file', 'file_name', 'file_type', 'file_size')
        }),
        ('النص المستخرج', {
            'fields': ('extracted_text',),
            'classes': ('collapse',)
        }),
        ('التواريخ', {
            'fields': ('uploaded_at',),
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

@admin.register(CriminalReport)
class CriminalReportAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'complainant_name', 'police_center', 'complaint_type', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'police_center', 'complaint_type', 'created_at']
    search_fields = ['reference_number', 'complainant_name', 'complainant_phone', 'complainant_email']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['reference_number', 'created_at', 'updated_at', 'reserved_at']
    
    fieldsets = (
        ('رقم المرجع', {
            'fields': ('reference_number',)
        }),
        ('بيانات الشاكي', {
            'fields': ('complainant_name', 'complainant_id', 'complainant_phone', 'complainant_email')
        }),
        ('بيانات البلاغ', {
            'fields': ('police_center', 'complaint_type', 'status')
        }),
        ('تفاصيل الواقعة', {
            'fields': ('complaint_subject', 'incident_date', 'incident_time', 'incident_location', 'incident_lat', 'incident_lng'),
            'classes': ('collapse',)
        }),
        ('العلاقة والاتفاق', {
            'fields': ('relationship', 'agreement_type'),
            'classes': ('collapse',)
        }),
        ('المبالغ والممتلكات', {
            'fields': ('money_seized', 'seized_amount', 'seized_property'),
            'classes': ('collapse',)
        }),
        ('طريقة التحويل', {
            'fields': ('transfer_method', 'bank_name', 'account_number', 'other_transfer_method'),
            'classes': ('collapse',)
        }),
        ('الشهود والإثباتات', {
            'fields': ('has_witnesses', 'witnesses_info', 'has_evidence', 'evidence_description'),
            'classes': ('collapse',)
        }),
        ('أقوال إضافية', {
            'fields': ('additional_statements',),
            'classes': ('collapse',)
        }),
        ('المشكو في حقهم', {
            'fields': ('accused_parties',),
            'classes': ('collapse',)
        }),
        ('إدارة البلاغ', {
            'fields': ('assigned_to', 'reserved_by', 'reserved_at', 'staff_notes')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CriminalReportActivity)
class CriminalReportActivityAdmin(admin.ModelAdmin):
    list_display = ['report', 'action_type', 'user', 'created_at']
    list_filter = ['action_type', 'created_at']
    search_fields = ['report__reference_number', 'description', 'user__username']
    readonly_fields = ['report', 'action_type', 'user', 'description', 'old_value', 'new_value', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(ReportNote)
class ReportNoteAdmin(admin.ModelAdmin):
    list_display = ['report', 'note_type', 'created_by', 'created_at', 'is_deleted']
    list_filter = ['note_type', 'is_deleted', 'created_at']
    search_fields = ['report__reference_number', 'content', 'created_by__username']
    readonly_fields = ['report', 'note_type', 'content', 'created_by', 'created_at']
    
    def has_add_permission(self, request):
        return False

@admin.register(BankContactRequest)
class BankContactRequestAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'center', 'report_number', 'report_year', 'status', 'created_at']
    list_filter = ['status', 'center', 'created_at']
    search_fields = ['bank_name', 'report_number', 'account_number', 'charge']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
