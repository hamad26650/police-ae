"""
نظام إرسال البريد الإلكتروني
Email Service for Sending Notifications
"""

import logging
from django.core.mail import send_mail
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
                'message': 'تم حفظ الرد بنجاح. لتفعيل إرسال الإيميلات، يرجى إضافة إعدادات البريد الإلكتروني في DigitalOcean Variables.'
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
            
            # تحديد البريد الإلكتروني الصحيح
            recipient_email = inquiry.email if inquiry.email else inquiry.phone
            
            # التحقق من صحة البريد الإلكتروني
            if not recipient_email or '@' not in recipient_email:
                logger.error(f'البريد الإلكتروني غير صحيح للاستعلام {inquiry.get_inquiry_id()}: {recipient_email}')
                return {
                    'success': False,
                    'message': 'البريد الإلكتروني غير صحيح. لم يتم إرسال الرسالة.'
                }
            
            # إرسال الرسالة
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'✅ تم إرسال بريد إلكتروني للاستعلام {inquiry.get_inquiry_id()} إلى {recipient_email}')
            
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
                user_message = 'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني: خطأ في المصادقة. تحقق من EMAIL_HOST_USER وEMAIL_HOST_PASSWORD في DigitalOcean Variables.'
            elif 'timeout' in error_msg.lower():
                user_message = 'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني: انتهت مهلة الاتصال.'
            else:
                user_message = f'تم حفظ الرد بنجاح. فشل إرسال البريد الإلكتروني: {error_msg[:100]}'
            
            return {
                'success': True,  # الرد محفوظ، فقط الإيميل فشل
                'message': user_message
            }
    
    @staticmethod
    def send_inquiry_confirmation(inquiry):
        """إرسال إيميل تأكيد للمواطن عند تقديم استعلام"""
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning('إعدادات البريد الإلكتروني غير مكتملة')
            return {'success': False, 'message': 'إعدادات البريد الإلكتروني غير مكتملة'}
        
        try:
            import socket
            socket.setdefaulttimeout(10)
            
            subject = f'تأكيد استلام استعلامكم - رقم {inquiry.get_inquiry_id()}'
            
            html_message = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>تأكيد استلام الاستعلام</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #4a90e2; color: white; padding: 20px; text-align: center; }}
        .content {{ background: #f8f9fa; padding: 20px; }}
        .footer {{ background: #343a40; color: white; padding: 15px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>شرطة الشارقة</h2>
            <p>تأكيد استلام الاستعلام</p>
        </div>
        <div class="content">
            <h3>عزيزي المواطن،</h3>
            <p>نؤكد لكم استلام استعلامكم بخصوص البلاغ رقم <strong>{inquiry.report_number}/{inquiry.report_year}</strong></p>
            <p><strong>رقم الاستعلام:</strong> {inquiry.get_inquiry_id()}</p>
            <p><strong>مركز الشرطة:</strong> {inquiry.police_center}</p>
            <p><strong>تاريخ الاستعلام:</strong> {inquiry.created_at.strftime('%Y-%m-%d %H:%M')}</p>
            <p>سيتم التواصل معكم قريباً عبر البريد الإلكتروني المرفق.</p>
            <p>شكراً لثقتكم بنا.</p>
        </div>
        <div class="footer">
            <p>شرطة الشارقة - خدمة المواطنين</p>
        </div>
    </div>
</body>
</html>
            """
            
            plain_message = f"""
تأكيد استلام الاستعلام
رقم الاستعلام: {inquiry.get_inquiry_id()}
مركز الشرطة: {inquiry.police_center}
رقم البلاغ: {inquiry.report_number}/{inquiry.report_year}
تاريخ الاستعلام: {inquiry.created_at.strftime('%Y-%m-%d %H:%M')}

سيتم التواصل معكم قريباً.
شكراً لثقتكم بنا.
شرطة الشارقة
            """
            
            # تحديد البريد الإلكتروني الصحيح
            recipient_email = inquiry.email if inquiry.email else inquiry.phone
            
            if not recipient_email or '@' not in recipient_email:
                logger.warning(f'البريد الإلكتروني غير صحيح للاستعلام {inquiry.get_inquiry_id()}')
                return {'success': False, 'message': 'البريد الإلكتروني غير صحيح'}
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f'✅ تم إرسال إيميل تأكيد للاستعلام {inquiry.get_inquiry_id()} إلى {recipient_email}')
            return {'success': True, 'message': 'تم إرسال الإيميل بنجاح'}
            
        except Exception as e:
            logger.error(f'فشل إرسال إيميل تأكيد: {str(e)}')
            return {'success': False, 'message': f'فشل إرسال الإيميل: {str(e)}'}
    
    @staticmethod
    def notify_staff_new_inquiry(inquiry):
        """إرسال إشعار للموظفين عن استعلام جديد"""
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning('إعدادات البريد الإلكتروني غير مكتملة')
            return {'success': False, 'message': 'إعدادات البريد الإلكتروني غير مكتملة'}
        
        try:
            from django.contrib.auth.models import User
            import socket
            socket.setdefaulttimeout(10)
            
            # الحصول على جميع الموظفين
            staff_users = User.objects.filter(is_staff=True, is_active=True)
            
            if not staff_users.exists():
                logger.warning('لا يوجد موظفين مفعلين لإرسال الإشعار')
                return {'success': False, 'message': 'لا يوجد موظفين مفعلين'}
            
            subject = f'استعلام جديد - رقم {inquiry.get_inquiry_id()}'
            
            html_message = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>استعلام جديد</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #dc3545; color: white; padding: 20px; text-align: center; }}
        .content {{ background: #f8f9fa; padding: 20px; }}
        .footer {{ background: #343a40; color: white; padding: 15px; text-align: center; }}
        .urgent {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔔 استعلام جديد</h2>
            <p>نظام إدارة الاستعلامات</p>
        </div>
        <div class="content">
            <div class="urgent">
                <h3>⚠️ يرجى الرد على هذا الاستعلام</h3>
            </div>
            <p><strong>رقم الاستعلام:</strong> {inquiry.get_inquiry_id()}</p>
            <p><strong>نوع الاستعلام:</strong> {inquiry.get_inquiry_type_display()}</p>
            <p><strong>مركز الشرطة:</strong> {inquiry.police_center}</p>
            <p><strong>رقم البلاغ:</strong> {inquiry.report_number}/{inquiry.report_year}</p>
            <p><strong>البريد الإلكتروني:</strong> {inquiry.phone}</p>
            <p><strong>تاريخ الاستعلام:</strong> {inquiry.created_at.strftime('%Y-%m-%d %H:%M')}</p>
            <p><strong>رسالة الاستعلام:</strong> {inquiry.message}</p>
            <hr>
            <p><a href="https://octopus-app-glkh4.ondigitalocean.app/staff/dashboard/" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">الرد على الاستعلام</a></p>
        </div>
        <div class="footer">
            <p>نظام إدارة الاستعلامات - شرطة الشارقة</p>
        </div>
    </div>
</body>
</html>
            """
            
            plain_message = f"""
استعلام جديد - رقم {inquiry.get_inquiry_id()}

نوع الاستعلام: {inquiry.get_inquiry_type_display()}
مركز الشرطة: {inquiry.police_center}
رقم البلاغ: {inquiry.report_number}/{inquiry.report_year}
البريد الإلكتروني: {inquiry.phone}
تاريخ الاستعلام: {inquiry.created_at.strftime('%Y-%m-%d %H:%M')}
رسالة الاستعلام: {inquiry.message}

يرجى الرد على هذا الاستعلام من خلال لوحة التحكم.
            """
            
            # إرسال الإيميل لجميع الموظفين
            staff_emails = [user.email for user in staff_users if user.email]
            
            if staff_emails:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=staff_emails,
                    html_message=html_message,
                    fail_silently=False
                )
                
                logger.info(f'تم إرسال إشعار للموظفين عن الاستعلام {inquiry.get_inquiry_id()} إلى {len(staff_emails)} موظف')
                return {'success': True, 'message': f'تم إرسال الإشعار إلى {len(staff_emails)} موظف'}
            else:
                logger.warning('لا توجد عناوين بريد إلكتروني للموظفين')
                return {'success': False, 'message': 'لا توجد عناوين بريد إلكتروني للموظفين'}
            
        except Exception as e:
            logger.error(f'فشل إرسال إشعار للموظفين: {str(e)}')
            return {'success': False, 'message': f'فشل إرسال الإشعار: {str(e)}'}
    
    @staticmethod
    def send_request_confirmation(service_request):
        """إرسال إيميل تأكيد لطلب خدمة"""
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning('إعدادات البريد الإلكتروني غير مكتملة')
            return {'success': False, 'message': 'إعدادات البريد الإلكتروني غير مكتملة'}
        
        try:
            import socket
            socket.setdefaulttimeout(10)
            
            subject = f'تأكيد استلام طلبكم - رقم {service_request.get_request_id()}'
            
            html_message = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>تأكيد استلام الطلب</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #28a745; color: white; padding: 20px; text-align: center; }}
        .content {{ background: #f8f9fa; padding: 20px; }}
        .footer {{ background: #343a40; color: white; padding: 15px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>شرطة الشارقة</h2>
            <p>تأكيد استلام الطلب</p>
        </div>
        <div class="content">
            <h3>عزيزي المواطن،</h3>
            <p>نؤكد لكم استلام طلبكم بنجاح</p>
            <p><strong>رقم الطلب:</strong> {service_request.get_request_id()}</p>
            <p><strong>الخدمة:</strong> {service_request.service}</p>
            <p><strong>المركز:</strong> {service_request.center}</p>
            <p><strong>الاسم:</strong> {service_request.requester_name}</p>
            <p><strong>البريد الإلكتروني:</strong> {service_request.requester_email}</p>
            <p><strong>رقم الهاتف:</strong> {service_request.requester_phone}</p>
            <p><strong>تفاصيل الطلب:</strong> {service_request.request_details}</p>
            <p><strong>تاريخ الطلب:</strong> {service_request.created_at.strftime('%Y-%m-%d %H:%M')}</p>
            <p>سيتم التواصل معكم قريباً لتحديث حالة الطلب.</p>
            <p>شكراً لثقتكم بنا.</p>
        </div>
        <div class="footer">
            <p>شرطة الشارقة - خدمة المواطنين</p>
        </div>
    </div>
</body>
</html>
            """
            
            plain_message = f"""
تأكيد استلام الطلب
رقم الطلب: {service_request.get_request_id()}
الخدمة: {service_request.service}
المركز: {service_request.center}
الاسم: {service_request.requester_name}
البريد الإلكتروني: {service_request.requester_email}
رقم الهاتف: {service_request.requester_phone}
تفاصيل الطلب: {service_request.request_details}
تاريخ الطلب: {service_request.created_at.strftime('%Y-%m-%d %H:%M')}

سيتم التواصل معكم قريباً.
شكراً لثقتكم بنا.
شرطة الشارقة
            """
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[service_request.requester_email],
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f'تم إرسال إيميل تأكيد للطلب {service_request.get_request_id()}')
            return {'success': True, 'message': 'تم إرسال الإيميل بنجاح'}
            
        except Exception as e:
            logger.error(f'فشل إرسال إيميل تأكيد للطلب: {str(e)}')
            return {'success': False, 'message': f'فشل إرسال الإيميل: {str(e)}'}
    
    @staticmethod
    def send_bank_contact_request(bank_request):
        """
        إرسال طلب مخاطبة البنك إلى البنك المحدد
        
        Args:
            bank_request: كائن BankContactRequest
        
        Returns:
            dict: نتيجة الإرسال {'success': bool, 'message': str}
        """
        # قاموس الإيميلات الخاصة بكل بنك
        BANK_EMAILS = {
            'بنك ابوظبي التجاري': 'Project.test85@outlook.com',
            'مصرف ابوظبي الاسلامي': 'Project.test85@outlook.com',
            'بنك دبي الاسلامي': 'Project.test85@outlook.com',
        }
        
        # التحقق من إعدادات البريد الإلكتروني
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning('إعدادات البريد الإلكتروني غير مكتملة - تم حفظ الطلب بدون إرسال إيميل')
            return {
                'success': True,
                'message': 'تم حفظ الطلب بنجاح. لتفعيل إرسال الإيميلات، يرجى إضافة إعدادات البريد الإلكتروني.'
            }
        
        try:
            import socket
            socket.setdefaulttimeout(10)
            
            # الحصول على إيميل البنك
            bank_email = BANK_EMAILS.get(bank_request.bank_name)
            
            if not bank_email:
                logger.warning(f'لا يوجد إيميل مسجل للبنك: {bank_request.bank_name}')
                return {
                    'success': False,
                    'message': f'لا يوجد إيميل مسجل للبنك: {bank_request.bank_name}'
                }
            
            center_email = bank_request.center.email if bank_request.center and bank_request.center.email else None
            recipients = [bank_email]
            if center_email and center_email not in recipients:
                recipients.append(center_email)
            
            # عنوان الرسالة
            subject = f'طلب مخاطبة من مركز شرطة - البلاغ رقم {bank_request.report_number}/{bank_request.report_year}'
            
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
        .request-info {{
            background-color: #f8f9fb;
            border-right: 4px solid #4a90e2;
            padding: 15px 20px;
            margin-bottom: 25px;
            border-radius: 8px;
        }}
        .request-info h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 16px;
        }}
        .request-info p {{
            margin: 8px 0;
            color: #555;
            font-size: 14px;
        }}
        .request-info strong {{
            color: #2c3e50;
        }}
        .details-box {{
            background-color: #ffffff;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .details-box h3 {{
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 16px;
        }}
        .details-text {{
            color: #2c3e50;
            line-height: 1.8;
            font-size: 15px;
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
            <div class="request-info">
                <h3>📋 طلب مخاطبة البنك</h3>
                <p><strong>اسم البنك:</strong> {bank_request.bank_name}</p>
                <p><strong>مركز الاختصاص:</strong> {bank_request.center.name}</p>
                <p><strong>رقم البلاغ:</strong> {bank_request.report_number}/{bank_request.report_year}</p>
                <p><strong>التهمة:</strong> {bank_request.charge}</p>
                <p><strong>رقم الحساب:</strong> {bank_request.account_number}</p>
                <p><strong>تاريخ الطلب:</strong> {bank_request.created_at.strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            
            <div class="details-box">
                <h3>📝 تفاصيل الطلب</h3>
                <div class="details-text">
                    <p>نرجو منكم التكرم بالتعاون معنا في هذا الطلب المتعلق بالبلاغ رقم <strong>{bank_request.report_number}/{bank_request.report_year}</strong>.</p>
                    <p><strong>التهمة:</strong> {bank_request.charge}</p>
                    <p><strong>رقم الحساب:</strong> {bank_request.account_number}</p>
                    <p>يرجى التواصل معنا في أقرب وقت ممكن.</p>
                </div>
            </div>
            
            <div class="divider"></div>
            
            <p style="color: #7f8c8d; font-size: 14px; text-align: center;">
                نشكركم على تعاونكم معنا.
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

طلب مخاطبة البنك

اسم البنك: {bank_request.bank_name}
مركز الاختصاص: {bank_request.center.name}
رقم البلاغ: {bank_request.report_number}/{bank_request.report_year}
التهمة: {bank_request.charge}
رقم الحساب: {bank_request.account_number}
تاريخ الطلب: {bank_request.created_at.strftime('%Y-%m-%d %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نرجو منكم التكرم بالتعاون معنا في هذا الطلب المتعلق بالبلاغ رقم {bank_request.report_number}/{bank_request.report_year}.

التهمة: {bank_request.charge}
رقم الحساب: {bank_request.account_number}

يرجى التواصل معنا في أقرب وقت ممكن.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

نشكركم على تعاونكم معنا.

مركز شرطة البحيرة
الشارقة - دولة الإمارات العربية المتحدة
info@police.ae | +971-6-123-4567
            """
            
            # إرسال الرسالة
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'✅ تم إرسال طلب مخاطبة البنك {bank_request.id} إلى {", ".join(recipients)}')
            
            return {
                'success': True,
                'message': f'تم إرسال الطلب إلى {bank_request.bank_name} بنجاح'
            }
            
        except socket.timeout:
            logger.error(f'انتهت مهلة الاتصال بخادم البريد الإلكتروني لطلب مخاطبة البنك {bank_request.id}')
            return {
                'success': True,
                'message': 'تم حفظ الطلب بنجاح. فشل إرسال البريد الإلكتروني بسبب انتهاء المهلة. تحقق من إعدادات SMTP.'
            }
        except Exception as e:
            error_msg = str(e)
            logger.error(f'فشل إرسال البريد الإلكتروني لطلب مخاطبة البنك {bank_request.id}: {error_msg}')
            
            # رسائل خطأ واضحة
            if 'Authentication' in error_msg or '535' in error_msg:
                user_message = 'تم حفظ الطلب بنجاح. فشل إرسال البريد الإلكتروني: خطأ في المصادقة. تحقق من EMAIL_HOST_USER وEMAIL_HOST_PASSWORD.'
            elif 'timeout' in error_msg.lower():
                user_message = 'تم حفظ الطلب بنجاح. فشل إرسال البريد الإلكتروني: انتهت مهلة الاتصال.'
            else:
                user_message = f'تم حفظ الطلب بنجاح. فشل إرسال البريد الإلكتروني: {error_msg[:100]}'
            
            return {
                'success': True,
                'message': user_message
            }


# إنشاء instance من الخدمة
email_service = EmailService()

