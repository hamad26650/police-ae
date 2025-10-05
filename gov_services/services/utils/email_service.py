"""
نظام إرسال البريد الإلكتروني
Email Service for Sending Notifications
"""

import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger('services')


class EmailService:
    """خدمة إرسال البريد الإلكتروني"""
    
    @staticmethod
    def send_inquiry_response(inquiry, response_text):
        """
        إرسال رد على استعلام المتعامل عبر البريد الإلكتروني
        
        Args:
            inquiry: كائن الاستعلام
            response_text: نص الرد
        
        Returns:
            dict: نتيجة الإرسال {'success': bool, 'message': str}
        """
        # التحقق من إعدادات البريد الإلكتروني
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning('إعدادات البريد الإلكتروني غير مكتملة - تم حفظ الرد بدون إرسال إيميل')
            return {
                'success': True,  # نعتبرها ناجحة لأن الرد تم حفظه
                'message': 'تم حفظ الرد بنجاح. لتفعيل إرسال الإيميلات، يرجى إضافة إعدادات البريد الإلكتروني في Railway Variables.'
            }
        
        try:
            import socket
            # تعيين timeout عام للـ socket لمنع التعليق
            socket.setdefaulttimeout(10)
            # عنوان الرسالة
            subject = f'رد على استعلامكم - مركز شرطة البحيرة - رقم {inquiry.get_inquiry_id()}'
            
            # محتوى الرسالة (HTML)
            html_message = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
            margin: 0;
            padding: 20px;
            direction: rtl;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 700;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 14px;
            opacity: 0.95;
        }}
        .content {{
            padding: 30px 20px;
        }}
        .inquiry-info {{
            background-color: #f8f9fb;
            border-right: 4px solid #4a90e2;
            padding: 15px 20px;
            margin-bottom: 25px;
            border-radius: 8px;
        }}
        .inquiry-info h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 16px;
        }}
        .inquiry-info p {{
            margin: 8px 0;
            color: #555;
            font-size: 14px;
        }}
        .inquiry-info strong {{
            color: #2c3e50;
        }}
        .response-box {{
            background-color: #ffffff;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .response-box h3 {{
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 16px;
        }}
        .response-text {{
            color: #2c3e50;
            line-height: 1.8;
            font-size: 15px;
            white-space: pre-wrap;
        }}
        .footer {{
            background-color: #f8f9fb;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #e1e8ed;
        }}
        .footer p {{
            margin: 5px 0;
            color: #7f8c8d;
            font-size: 13px;
        }}
        .divider {{
            height: 1px;
            background-color: #e1e8ed;
            margin: 25px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚓 مركز شرطة البحيرة</h1>
            <p>الشارقة - دولة الإمارات العربية المتحدة</p>
        </div>
        
        <div class="content">
            <div class="inquiry-info">
                <h3>📋 تفاصيل الاستعلام</h3>
                <p><strong>رقم الاستعلام:</strong> {inquiry.get_inquiry_id()}</p>
                <p><strong>رقم البلاغ:</strong> {inquiry.report_number}/{inquiry.report_year}</p>
                <p><strong>مركز الشرطة:</strong> {inquiry.police_center}</p>
            </div>
            
            <div class="response-box">
                <h3>✉️ الرد على استعلامكم</h3>
                <div class="response-text">{response_text}</div>
            </div>
            
            <div class="divider"></div>
            
            <p style="color: #7f8c8d; font-size: 14px; text-align: center;">
                نشكركم على تواصلكم معنا. للاستفسارات الإضافية، يرجى التواصل معنا عبر القنوات الرسمية.
            </p>
        </div>
        
        <div class="footer">
            <p><strong>مركز شرطة البحيرة</strong></p>
            <p>📧 info@police.ae | 📞 +971-6-123-4567</p>
            <p style="margin-top: 15px; font-size: 12px;">
                © 2024 مركز شرطة البحيرة. جميع الحقوق محفوظة.
            </p>
        </div>
    </div>
</body>
</html>
"""
            
            # النص البسيط (للإيميلات التي لا تدعم HTML)
            plain_message = f"""
مركز شرطة البحيرة
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

تفاصيل الاستعلام:
• رقم الاستعلام: {inquiry.get_inquiry_id()}
• رقم البلاغ: {inquiry.report_number}/{inquiry.report_year}
• مركز الشرطة: {inquiry.police_center}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

الرد على استعلامكم:

{response_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نشكركم على تواصلكم معنا.

مركز شرطة البحيرة
الشارقة - دولة الإمارات العربية المتحدة
info@police.ae | +971-6-123-4567
"""
            
            # إرسال الرسالة
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.phone],  # حقل phone يحتوي على الإيميل
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'تم إرسال بريد إلكتروني للاستعلام {inquiry.get_inquiry_id()} إلى {inquiry.phone}')
            
            return {
                'success': True,
                'message': 'تم إرسال الرد والبريد الإلكتروني بنجاح'
            }
            
        except socket.timeout:
            logger.error(f'انتهت مهلة الاتصال بخادم البريد الإلكتروني للاستعلام {inquiry.get_inquiry_id()}')
            return {
                'success': True,  # الرد محفوظ، فقط الإيميل فشل
                'message': 'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني بسبب انتهاء المهلة. تحقق من إعدادات SMTP.'
            }
        except Exception as e:
            error_msg = str(e)
            logger.error(f'فشل إرسال البريد الإلكتروني للاستعلام {inquiry.get_inquiry_id()}: {error_msg}')
            
            # رسائل خطأ واضحة للمستخدم
            if 'Authentication' in error_msg or '535' in error_msg:
                user_message = 'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني: خطأ في المصادقة. تحقق من EMAIL_HOST_USER وEMAIL_HOST_PASSWORD في Railway Variables.'
            elif 'timeout' in error_msg.lower():
                user_message = 'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني: انتهت مهلة الاتصال.'
            else:
                user_message = f'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني: {error_msg[:100]}'
            
            return {
                'success': True,  # الرد محفوظ، فقط الإيميل فشل
                'message': user_message
            }


# إنشاء instance من الخدمة
email_service = EmailService()

