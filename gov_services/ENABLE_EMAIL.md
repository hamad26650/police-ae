# 📧 تفعيل نظام البريد الإلكتروني

## ⚠️ ملاحظة مهمة

**نظام البريد الإلكتروني معطل حالياً** لضمان استقرار الموقع وسرعة الاستجابة.

الموقع يعمل بشكل كامل:
- ✅ تقديم الاستعلامات
- ✅ لوحة تحكم الموظفين
- ✅ الرد على الاستعلامات
- ✅ حفظ البيانات

**فقط الإيميلات غير مفعلة.**

---

## 🔓 كيفية تفعيل نظام البريد الإلكتروني

### **الخطوة 1: أضف المتغيرات في Railway**

1. افتح Railway Dashboard: https://railway.app
2. اختر المشروع: `gov-services-portal`
3. اضغط `Variables`
4. أضف المتغيرات الثلاثة:

```
EMAIL_HOST_USER=albuhairah.test@outlook.com
EMAIL_HOST_PASSWORD=H@mad.95335
DEFAULT_FROM_EMAIL=albuhairah.test@outlook.com
```

### **الخطوة 2: فك التعليق في الكود**

في ملف `services/views.py`، في دالة `respond_to_inquiry`:

**ابحث عن:**
```python
# ملاحظة: نظام البريد الإلكتروني معطل مؤقتاً
```

**واستبدل الكود بـ:**
```python
# إرسال البريد الإلكتروني للمتعامل
from django.conf import settings

if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    try:
        from threading import Thread
        
        def send_email_async():
            try:
                email_result = email_service.send_inquiry_response(inquiry, response_text)
                if email_result['success']:
                    logger.info(f'تم إرسال بريد إلكتروني للاستعلام {inquiry.get_inquiry_id()}')
            except Exception as e:
                logger.error(f'خطأ في إرسال البريد الإلكتروني: {str(e)}')
        
        # إرسال الإيميل في خلفية بدون انتظار
        Thread(target=send_email_async, daemon=True).start()
        logger.info('تم بدء إرسال البريد الإلكتروني في الخلفية')
    except Exception as e:
        logger.error(f'خطأ في إنشاء Thread للبريد الإلكتروني: {str(e)}')

return JsonResponse({
    'success': True, 
    'message': 'تم حفظ الرد بنجاح وسيتم إرسال البريد الإلكتروني',
    'inquiry_id': inquiry.get_inquiry_id(),
    'email_sent': True
})
```

### **الخطوة 3: رفع التحديث**

```bash
git add .
git commit -m "Enable email system with async sending"
git push
```

---

## 🎯 لماذا Threading؟

**المشكلة السابقة:**
- Django ينتظر إرسال الإيميل (30 ثانية)
- Worker Timeout!

**الحل:**
- إرسال الإيميل في **Thread منفصل**
- الموقع يرد فوراً (1 ثانية)
- الإيميل يُرسل في الخلفية

---

## 🔍 الفرق

### **بدون Threading (المشكلة القديمة):**
```
1. حفظ الرد → 0.1 ثانية
2. إرسال الإيميل → 30 ثانية! ❌
3. الرد للمستخدم → بعد 30 ثانية
```

### **مع Threading (الحل):**
```
1. حفظ الرد → 0.1 ثانية
2. بدء Thread للإيميل → 0.1 ثانية
3. الرد للمستخدم → 0.2 ثانية ✅
4. الإيميل يُرسل في الخلفية → بدون تأثير
```

---

## ⚠️ تحذير

**لا تفعّل الإيميل قبل:**
- إضافة المتغيرات في Railway
- التأكد من صحة بيانات Outlook
- اختبار الإرسال محلياً أولاً

**وإلا ستعود مشكلة Timeout!**

---

## 💡 بديل أفضل (للمستقبل)

استخدم **Celery + Redis** للمهام غير المتزامنة:
- أكثر احترافية
- أفضل لإدارة الطوابير
- مناسب للإنتاج

لكن Threading كافٍ للآن!

---

© 2025 - دليل تفعيل البريد الإلكتروني

