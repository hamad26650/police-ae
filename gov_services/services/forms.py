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
    
    petition_text = forms.CharField(
        min_length=50,
        max_length=5000,
        required=False,
        error_messages={
            'min_length': 'نص العريضة قصير جداً (50 حرف على الأقل)',
            'max_length': 'نص العريضة طويل جداً (5000 حرف كحد أقصى)'
        },
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'اكتب نص العريضة كاملاً هنا... (اختياري)',
            'rows': 10
        })
    )
    
    attachments = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-input',
            'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx',
            'id': 'attachments'
        }),
        help_text='يمكنك رفع ملفات PDF، صور، أو مستندات Word (حد أقصى 10 ملفات، كل ملف حتى 5 MB)'
    )


# خيارات مراكز الاختصاص لمخاطبة البنوك
BANK_CONTACT_CENTER_CHOICES = [
    ('', '-- اختر مركز الاختصاص --'),
    ('مركز شرطة البحيرة', 'مركز شرطة البحيرة'),
    ('مركز شرطة الغرب', 'مركز شرطة الغرب'),
]


class BankContactForm(forms.Form):
    """نموذج مخاطبة البنوك"""
    
    center = forms.ChoiceField(
        choices=BANK_CONTACT_CENTER_CHOICES,
        required=True,
        error_messages={
            'required': 'يرجى اختيار مركز الاختصاص',
            'invalid_choice': 'مركز الاختصاص المختار غير صحيح'
        },
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'center'
        })
    )
    
    report_number = forms.IntegerField(
        min_value=1,
        max_value=9999,
        required=True,
        error_messages={
            'required': 'يرجى إدخال رقم البلاغ',
            'invalid': 'رقم البلاغ يجب أن يكون رقماً',
            'min_value': 'رقم البلاغ يجب أن يكون 1 على الأقل',
            'max_value': 'رقم البلاغ يجب أن يكون 9999 كحد أقصى'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'أدخل رقم البلاغ (1-9999)',
            'id': 'report_number',
            'min': '1',
            'max': '9999'
        })
    )
    
    report_year = forms.ChoiceField(
        choices=[
            ('', '-- اختر السنة --'),
            (2020, '2020'),
            (2021, '2021'),
            (2022, '2022'),
            (2023, '2023'),
            (2024, '2024'),
            (2025, '2025'),
        ],
        required=True,
        error_messages={
            'required': 'يرجى اختيار السنة',
            'invalid_choice': 'السنة المختارة غير صحيحة'
        },
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'report_year'
        })
    )
    
    charge = forms.ChoiceField(
        choices=[
            ('', '-- اختر التهمة --'),
            ('خيانة الامانة', 'خيانة الامانة'),
            ('السب', 'السب'),
            ('الاستيلاء', 'الاستيلاء'),
            ('التهديد', 'التهديد'),
        ],
        required=True,
        error_messages={
            'required': 'يرجى اختيار التهمة',
            'invalid_choice': 'الخيار المحدد غير صحيح'
        },
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'charge'
        })
    )
    
    bank_name = forms.ChoiceField(
        choices=[
            ('', '-- اختر اسم البنك --'),
            ('بنك ابوظبي التجاري', 'بنك ابوظبي التجاري'),
            ('مصرف ابوظبي الاسلامي', 'مصرف ابوظبي الاسلامي'),
            ('بنك دبي الاسلامي', 'بنك دبي الاسلامي'),
        ],
        required=True,
        error_messages={
            'required': 'يرجى اختيار اسم البنك',
            'invalid_choice': 'الخيار المحدد غير صحيح'
        },
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'bank_name'
        })
    )
    
    account_number = forms.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'يرجى إدخال رقم الحساب',
            'max_length': 'رقم الحساب طويل جداً'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'أدخل رقم الحساب',
            'id': 'account_number'
        })
    )