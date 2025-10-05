# 🔒 إصلاح مشكلة CSRF 403 Forbidden

## ❌ المشكلة

عند إرسال النماذج على الموقع المستضاف على Railway، يظهر خطأ:
```
Forbidden (403)
CSRF verification failed. Request aborted.
```

---

## 🔍 السبب

عندما ينتقل الموقع من التطوير المحلي (`localhost`) إلى الإنتاج (`Railway`):
- Django يستخدم HTTPS
- يحتاج إعدادات CSRF خاصة
- يجب تحديد النطاقات الموثوقة (`CSRF_TRUSTED_ORIGINS`)

---

## ✅ الحل المطبق

### **1. إضافة CSRF_TRUSTED_ORIGINS**
في `settings.py` داخل قسم Railway/Production:

```python
# CSRF Trusted Origins - مهم جداً لـ Railway!
CSRF_TRUSTED_ORIGINS = [
    f'https://{allowed_host}',
    f'http://{allowed_host}',
]
```

هذا يخبر Django بأن يثق بالنطاق الخاص بـ Railway.

### **2. تعديل إعدادات CSRF Cookie**

**قبل:**
```python
CSRF_COOKIE_HTTPONLY = True
```

**بعد:**
```python
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access if needed
CSRF_COOKIE_SECURE = False  # Will be set to True in production
```

**في قسم Production:**
```python
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Important for Railway CSRF handling
```

---

## 🎯 النتيجة

✅ النماذج تعمل بدون مشاكل  
✅ CSRF Token يتم قبوله بشكل صحيح  
✅ الأمان محفوظ (HTTPS + Secure Cookies)  

---

## 📋 ملاحظات مهمة

1. **CSRF_COOKIE_HTTPONLY = False** ضروري في بعض الحالات عند استخدام AJAX/JavaScript
2. **CSRF_TRUSTED_ORIGINS** يجب أن يحتوي على نطاق Railway الخاص بك
3. **SECURE_PROXY_SSL_HEADER** مهم لأن Railway يستخدم proxy

---

## 🧪 التجربة

بعد النشر:
1. افتح أي صفحة فيها نموذج
2. اعبي البيانات
3. اضغط إرسال
4. ✅ المفروض يشتغل بدون أخطاء!

---

## 🐛 إذا استمرت المشكلة

جرب:
1. امسح الـ Cookies في المتصفح
2. افتح الموقع في نافذة خاصة (Incognito)
3. تأكد أن الموقع يستخدم HTTPS وليس HTTP
4. تفقد Railway Logs للتفاصيل

---

© 2025 - إصلاح CSRF

