"""
نماذج التحقق من صحة المدخلات (Input Validation)
"""
from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import datetime

# خيارات مراكز الشرطة
POLICE_CENTER_CHOICES = [
    ('', '-- اختر مركز الشرطة --'),
    ('مركز شرطة واسط الشامل', 'مركز شرطة واسط الشامل'),
    ('مركز شرطة الغرب الشامل', 'مركز شرطة الغرب الشامل'),
    ('مركز شرطة البحيرة الشامل', 'مركز شرطة البحيرة الشامل'),
    ('مركز شرطة الصناعية الشامل', 'مركز شرطة الصناعية الشامل'),
    ('مركز شرطة الصجعة الشامل', 'مركز شرطة الصجعة الشامل'),
    ('مركز شرطة السيوح الشامل', 'مركز شرطة السيوح الشامل'),
]

# Validator لرقم الهاتف الإماراتي
phone_validator = RegexValidator(
    regex=r'^(05|04)\d{8}$',
    message='رقم الهاتف يجب أن يبدأ بـ 05 أو 04 ويتكون من 10 أرقام'
)


class InquiryForm(forms.Form):
    """نموذج الاستعلام عن البلاغ"""
    
    police_center = forms.ChoiceField(
        choices=POLICE_CENTER_CHOICES,
        required=True,
        error_messages={
            'required': 'يرجى اختيار مركز الشرطة',
            'invalid_choice': 'مركز الشرطة المختار غير صحيح'
        },
        widget=forms.Select(attrs={
            'class': 'form-input'
        })
    )
    
    report_number = forms.IntegerField(
        min_value=1,
        max_value=9999,
        required=True,
        error_messages={
            'required': 'يرجى إدخال رقم البلاغ',
            'invalid': 'رقم البلاغ يجب أن يكون رقماً',
            'min_value': 'رقم البلاغ يجب أن يكون أكبر من 0',
            'max_value': 'رقم البلاغ يجب أن يكون أقل من 10000'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'أدخل رقم البلاغ (1-9999)',
            'min': '1',
            'max': '9999'
        })
    )
    
    report_year = forms.IntegerField(
        min_value=2020,
        max_value=datetime.now().year + 1,
        required=True,
        error_messages={
            'required': 'يرجى اختيار السنة',
            'invalid': 'السنة يجب أن تكون رقماً',
            'min_value': 'السنة يجب أن تكون من 2020 فما فوق',
            'max_value': f'السنة يجب أن تكون حتى {datetime.now().year + 1}'
        },
        widget=forms.Select(attrs={
            'class': 'form-input'
        })
    )
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        error_messages={
            'required': 'يرجى إدخال البريد الإلكتروني',
            'invalid': 'البريد الإلكتروني غير صحيح'
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'example@email.com',
            'dir': 'ltr'
        })
    )
    
    def clean_email(self):
        """تنظيف وتحقق من البريد الإلكتروني"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        return email
    
    def clean_report_number(self):
        """تنظيف وتحقق إضافي من رقم البلاغ"""
        number = self.cleaned_data.get('report_number')
        if number and (number < 1 or number > 9999):
            raise forms.ValidationError('رقم البلاغ يجب أن يكون بين 1 و 9999')
        return number


class StaffLoginForm(forms.Form):
    """نموذج تسجيل دخول الموظفين"""
    
    username = forms.CharField(
        max_length=150,
        required=True,
        error_messages={
            'required': 'يرجى إدخال اسم المستخدم',
            'max_length': 'اسم المستخدم طويل جداً'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'اسم المستخدم',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        max_length=128,
        required=True,
        error_messages={
            'required': 'يرجى إدخال كلمة المرور',
            'max_length': 'كلمة المرور طويلة جداً'
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'كلمة المرور',
            'autocomplete': 'current-password'
        })
    )


class InquiryResponseForm(forms.Form):
    """نموذج الرد على الاستعلام"""
    
    response = forms.CharField(
        min_length=10,
        max_length=1000,
        required=True,
        error_messages={
            'required': 'يرجى كتابة الرد',
            'min_length': 'الرد قصير جداً (10 أحرف على الأقل)',
            'max_length': 'الرد طويل جداً (1000 حرف كحد أقصى)'
        },
        widget=forms.Textarea(attrs={
            'class': 'response-textarea',
            'placeholder': 'اكتب ردك على الاستعلام...',
            'rows': 5
        })
    )
    
    def clean_response(self):
        """تنظيف نص الرد"""
        response = self.cleaned_data.get('response')
        if response:
            # إزالة المسافات الزائدة
            response = ' '.join(response.split())
            # التحقق من طول الرد بعد التنظيف
            if len(response) < 10:
                raise forms.ValidationError('الرد قصير جداً')
        return response


class ServiceRequestForm(forms.Form):
    """نموذج تقديم طلب خدمة"""
    
    requester_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'يرجى إدخال الاسم الكامل',
            'max_length': 'الاسم طويل جداً'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'الاسم الكامل'
        })
    )
    
    requester_email = forms.EmailField(
        max_length=254,
        required=True,
        error_messages={
            'required': 'يرجى إدخال البريد الإلكتروني',
            'invalid': 'البريد الإلكتروني غير صحيح'
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'example@email.com'
        })
    )
    
    requester_phone = forms.CharField(
        max_length=20,
        required=True,
        validators=[phone_validator],
        error_messages={
            'required': 'يرجى إدخال رقم الهاتف'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '05XXXXXXXX'
        })
    )
    
    requester_national_id = forms.CharField(
        max_length=20,
        required=True,
        error_messages={
            'required': 'يرجى إدخال رقم الهوية'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'رقم الهوية الإماراتية'
        })
    )
    
    request_details = forms.CharField(
        min_length=20,
        max_length=500,
        required=True,
        error_messages={
            'required': 'يرجى كتابة تفاصيل الطلب',
            'min_length': 'تفاصيل الطلب قصيرة جداً (20 حرف على الأقل)',
            'max_length': 'تفاصيل الطلب طويلة جداً (500 حرف كحد أقصى)'
        },
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'اشرح طلبك بالتفصيل...',
            'rows': 5
        })
    )