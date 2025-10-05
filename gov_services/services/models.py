from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# نموذج الخدمات الحكومية
class Service(models.Model):
    SERVICE_TYPES = [
        ('prosecution', 'النيابة العامة'),
        ('digital_id', 'الهوية الرقمية'),
        ('interior', 'وزارة الداخلية'),
        ('sharjah_police', 'شرطة الشارقة'),
        ('sharjah_municipality', 'بلدية الشارقة'),
    ]
    
    name = models.CharField(max_length=100, choices=SERVICE_TYPES, unique=True, verbose_name="اسم الخدمة")
    slug = models.SlugField(max_length=100, unique=True, default='default-slug', verbose_name="الرابط")
    description = models.TextField(verbose_name="وصف الخدمة")
    requirements = models.TextField(blank=True, null=True, verbose_name="المتطلبات")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="الرسوم")
    processing_time = models.PositiveIntegerField(default=5, verbose_name="مدة المعالجة (أيام)")
    icon = models.CharField(max_length=50, default="fas fa-building", verbose_name="أيقونة الخدمة")
    color = models.CharField(max_length=20, default="#007bff", verbose_name="لون البطاقة")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"
    
    def __str__(self):
        return dict(self.SERVICE_TYPES)[self.name]

# نموذج المراكز
class Center(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المركز")
    code = models.CharField(max_length=10, unique=True, verbose_name="رمز المركز")
    location = models.CharField(max_length=200, verbose_name="الموقع")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "مركز"
        verbose_name_plural = "المراكز"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

# نموذج الطلبات
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('under_review', 'تحت المراجعة'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('rejected', 'مرفوض'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('urgent', 'عاجلة'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="الخدمة")
    requester_name = models.CharField(max_length=100, verbose_name="اسم مقدم الطلب")
    requester_email = models.EmailField(verbose_name="البريد الإلكتروني")
    requester_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    requester_national_id = models.CharField(max_length=20, verbose_name="رقم الهوية")
    request_details = models.TextField(verbose_name="تفاصيل الطلب")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="الأولوية")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="مُسند إلى")
    center = models.ForeignKey(Center, on_delete=models.CASCADE, verbose_name="المركز")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    
    # حقول نظام الحجز
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='reserved_requests', verbose_name="محجوز بواسطة")
    reserved_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الحجز")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "طلب خدمة"
        verbose_name_plural = "طلبات الخدمات"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.name} - {self.requester_name}"
    
    def get_request_id(self):
        """إنشاء رقم طلب مُنسق"""
        return f"REQ-{self.id:06d}"
    
    def is_reserved(self):
        """التحقق من حجز الطلب"""
        return self.reserved_by is not None
    
    def can_be_reserved_by(self, user):
        """التحقق من إمكانية حجز الطلب بواسطة المستخدم"""
        return not self.is_reserved() or self.reserved_by == user

# نموذج الرسائل النصية
class SMSMessage(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, 
                               related_name='sms_messages', verbose_name="الطلب")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المرسل")
    message = models.TextField(verbose_name="نص الرسالة")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")
    is_sent = models.BooleanField(default=False, verbose_name="تم الإرسال")
    
    class Meta:
        verbose_name = "رسالة نصية"
        verbose_name_plural = "الرسائل النصية"
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"رسالة إلى {self.phone_number} - {self.request.get_request_id()}"

# نموذج الاستعلامات
class AuditLog(models.Model):
    """سجل التدقيق - Audit Trail"""
    ACTION_TYPES = [
        ('login', 'تسجيل دخول'),
        ('logout', 'تسجيل خروج'),
        ('view', 'عرض بيانات'),
        ('create', 'إنشاء'),
        ('update', 'تحديث'),
        ('delete', 'حذف'),
        ('export', 'تصدير'),
        ('failed_login', 'محاولة دخول فاشلة'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المستخدم")
    action = models.CharField(max_length=20, choices=ACTION_TYPES, verbose_name="الإجراء")
    model_name = models.CharField(max_length=100, blank=True, verbose_name="اسم النموذج")
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="معرف الكائن")
    description = models.TextField(verbose_name="الوصف")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="عنوان IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="التاريخ والوقت")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "سجل تدقيق"
        verbose_name_plural = "سجلات التدقيق"
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.user} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Inquiry(models.Model):
    INQUIRY_TYPES = [
        ('status', 'استعلام عن حالة طلب'),
        ('report_status', 'استعلام عن حالة بلاغ'),
        ('general', 'استعلام عام'),
        ('complaint', 'شكوى'),
        ('suggestion', 'اقتراح'),
    ]
    
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, verbose_name="نوع الاستعلام")
    full_name = models.CharField(max_length=100, blank=True, verbose_name="الاسم الكامل")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=254, verbose_name="البريد الإلكتروني / رقم الهاتف")
    request_reference = models.CharField(max_length=50, blank=True, verbose_name="رقم مرجعي للطلب")
    message = models.TextField(blank=True, verbose_name="الرسالة")
    
    # حقول الاستعلام عن البلاغ
    police_center = models.CharField(max_length=100, blank=True, verbose_name="مركز الشرطة")
    report_number = models.CharField(max_length=10, blank=True, verbose_name="رقم البلاغ")
    report_year = models.CharField(max_length=4, blank=True, verbose_name="سنة البلاغ")
    
    is_resolved = models.BooleanField(default=False, verbose_name="تم الحل")
    response = models.TextField(blank=True, verbose_name="الرد")
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="رد بواسطة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الحل")
    
    class Meta:
        verbose_name = "استعلام"
        verbose_name_plural = "الاستعلامات"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.inquiry_type == 'report_status':
            return f"استعلام عن بلاغ #{self.report_number}/{self.report_year} - {self.phone}"
        return f"{self.full_name} - {self.get_inquiry_type_display()}"
    
    def get_inquiry_id(self):
        """إنشاء رقم استعلام مُنسق"""
        return f"INQ-{self.id:06d}"

# نموذج إعدادات الموقع
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="بوابة الخدمات الحكومية", verbose_name="اسم الموقع")
    site_description = models.TextField(default="بوابة موحدة للخدمات الحكومية", verbose_name="وصف الموقع")
    contact_email = models.EmailField(default="info@gov.ae", verbose_name="بريد التواصل")
    contact_phone = models.CharField(max_length=20, default="+971-6-123-4567", verbose_name="هاتف التواصل")
    address = models.TextField(default="الشارقة، دولة الإمارات العربية المتحدة", verbose_name="العنوان")
    working_hours = models.CharField(max_length=100, default="الأحد - الخميس: 8:00 ص - 4:00 م", verbose_name="ساعات العمل")
    
    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"
    
    def __str__(self):
        return self.site_name

# نموذج ملف الموظف
class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'الإدارة'),
        ('center', 'المركز'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    employee_id = models.CharField(max_length=20, unique=True, blank=True, verbose_name="رقم الموظف")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='center', verbose_name="الدور")
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True, verbose_name="المركز")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    department = models.CharField(max_length=100, blank=True, verbose_name="القسم")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    def save(self, *args, **kwargs):
        # إنشاء رقم موظف تلقائي إذا لم يكن موجوداً
        if not self.employee_id:
            # استخدام ID المستخدم لإنشاء رقم موظف فريد
            self.employee_id = f"EMP-{self.user.id:05d}"
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "ملف موظف"
        verbose_name_plural = "ملفات الموظفين"
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"
    
    def can_view_all_requests(self):
        """تحديد ما إذا كان الموظف يمكنه رؤية جميع الطلبات"""
        return self.role == 'admin'
    
    def get_accessible_centers(self):
        """الحصول على المراكز التي يمكن للموظف الوصول إليها"""
        if self.role == 'admin':
            return Center.objects.filter(is_active=True)
        elif self.role == 'center' and self.center:
            return Center.objects.filter(id=self.center.id, is_active=True)
        return Center.objects.none()
