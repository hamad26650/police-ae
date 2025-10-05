"""
نظام إرسال الرسائل النصية عبر Twilio
SMS System using Twilio API
"""

import os
import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger('services')


class SMSService:
    """خدمة إرسال الرسائل النصية"""
    
    def __init__(self):
        """تهيئة Twilio Client"""
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.from_number = os.environ.get('TWILIO_PHONE_NUMBER')
        
        # التحقق من وجود الإعدادات
        if not all([self.account_sid, self.auth_token, self.from_number]):
            logger.warning('Twilio credentials not configured. SMS sending will be disabled.')
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)
    
    def send_inquiry_response(self, inquiry, response_text):
        """
        إرسال رد على استعلام المتعامل
        
        Args:
            inquiry: كائن الاستعلام
            response_text: نص الرد
        
        Returns:
            dict: نتيجة الإرسال {'success': bool, 'message': str, 'sid': str}
        """
        if not self.client:
            logger.error('SMS service not configured')
            return {
                'success': False,
                'message': 'خدمة الرسائل غير مفعلة',
                'sid': None
            }
        
        # تنسيق رقم الهاتف
        phone_number = self._format_phone_number(inquiry.phone)
        
        if not phone_number:
            logger.error(f'Invalid phone number: {inquiry.phone}')
            return {
                'success': False,
                'message': 'رقم الهاتف غير صحيح',
                'sid': None
            }
        
        # تجهيز نص الرسالة
        message_body = self._format_inquiry_response_message(inquiry, response_text)
        
        try:
            # إرسال الرسالة
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=phone_number
            )
            
            logger.info(f'SMS sent successfully to {phone_number}. SID: {message.sid}')
            
            return {
                'success': True,
                'message': 'تم إرسال الرسالة بنجاح',
                'sid': message.sid,
                'status': message.status
            }
            
        except TwilioRestException as e:
            logger.error(f'Twilio error: {e.msg} (Code: {e.code})')
            return {
                'success': False,
                'message': f'فشل إرسال الرسالة: {e.msg}',
                'sid': None,
                'error_code': e.code
            }
        
        except Exception as e:
            logger.error(f'Unexpected error sending SMS: {str(e)}')
            return {
                'success': False,
                'message': 'حدث خطأ غير متوقع أثناء إرسال الرسالة',
                'sid': None
            }
    
    def _format_phone_number(self, phone):
        """
        تنسيق رقم الهاتف إلى صيغة دولية
        
        Args:
            phone: رقم الهاتف
        
        Returns:
            str: رقم الهاتف بالصيغة الدولية أو None
        """
        if not phone:
            return None
        
        # إزالة المسافات والرموز غير الضرورية
        phone = ''.join(filter(str.isdigit, str(phone)))
        
        # إضافة مفتاح الإمارات إذا لم يكن موجوداً
        if phone.startswith('05'):
            phone = '971' + phone[1:]  # تحويل 05... إلى 9715...
        elif phone.startswith('5'):
            phone = '971' + phone  # تحويل 5... إلى 9715...
        elif not phone.startswith('971'):
            phone = '971' + phone  # إضافة +971
        
        # إضافة + في البداية
        return '+' + phone
    
    def _format_inquiry_response_message(self, inquiry, response_text):
        """
        تنسيق نص رسالة الرد على الاستعلام
        
        Args:
            inquiry: كائن الاستعلام
            response_text: نص الرد
        
        Returns:
            str: نص الرسالة المنسق
        """
        message = f"""مركز شرطة البحيرة
───────────────────
رقم الاستعلام: {inquiry.get_inquiry_id()}

عزيزي المتعامل،
تم الرد على استعلامكم بخصوص البلاغ رقم {inquiry.report_number}/{inquiry.report_year}:

"{response_text}"

شكراً لتواصلكم معنا
"""
        return message
    
    def send_custom_message(self, phone_number, message_text):
        """
        إرسال رسالة مخصصة
        
        Args:
            phone_number: رقم الهاتف
            message_text: نص الرسالة
        
        Returns:
            dict: نتيجة الإرسال
        """
        if not self.client:
            return {
                'success': False,
                'message': 'خدمة الرسائل غير مفعلة'
            }
        
        phone_number = self._format_phone_number(phone_number)
        
        if not phone_number:
            return {
                'success': False,
                'message': 'رقم الهاتف غير صحيح'
            }
        
        try:
            message = self.client.messages.create(
                body=message_text,
                from_=self.from_number,
                to=phone_number
            )
            
            return {
                'success': True,
                'message': 'تم إرسال الرسالة بنجاح',
                'sid': message.sid
            }
            
        except Exception as e:
            logger.error(f'Error sending custom SMS: {str(e)}')
            return {
                'success': False,
                'message': str(e)
            }


# إنشاء instance واحد من الخدمة
sms_service = SMSService()

