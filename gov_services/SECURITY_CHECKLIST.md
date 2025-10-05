# 🔒 قائمة التحقق الأمني

## ✅ قبل النشر (Production)

### إعدادات Django
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` من متغيرات البيئة
- [ ] `ALLOWED_HOSTS` محدد بالدومينات الصحيحة
- [ ] تغيير قاعدة البيانات من SQLite إلى PostgreSQL/MySQL
- [ ] تفعيل HTTPS (SSL Certificate)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`

### كلمات المرور
- [ ] تغيير كلمة مرور admin الافتراضية
- [ ] استخدام كلمات مرور قوية (12+ حرف)
- [ ] تفعيل Two-Factor Authentication للموظفين

### حماية البيانات
- [ ] تشفير البيانات الحساسة في قاعدة البيانات
- [ ] Backup يومي لقاعدة البيانات
- [ ] Rate Limiting على APIs
- [ ] Input Validation على جميع النماذج
- [ ] Output Sanitization لمنع XSS

### Monitoring & Logging
- [ ] تفعيل Logging للأحداث الأمنية
- [ ] مراقبة محاولات تسجيل الدخول الفاشلة
- [ ] تتبع الأخطاء باستخدام Sentry
- [ ] إعداد تنبيهات للنشاطات المشبوهة

### الخادم (Server)
- [ ] استخدام Gunicorn/uWSGI بدلاً من runserver
- [ ] Nginx/Apache كـ Reverse Proxy
- [ ] Firewall مفعل
- [ ] تحديثات أمنية منتظمة للنظام
- [ ] إخفاء إصدار Django من الـ Headers

### الشبكة
- [ ] استخدام HTTPS فقط
- [ ] إعداد CORS بشكل صحيح
- [ ] Content Security Policy (CSP)
- [ ] Clickjacking Protection

### الامتثال
- [ ] سياسة الخصوصية
- [ ] شروط الاستخدام
- [ ] GDPR compliance (إذا كان مطلوباً)
- [ ] توثيق API

## 🔧 أوامر مفيدة

### فحص الأمان
```bash
python manage.py check --deploy
```

### إنشاء SECRET_KEY جديد
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### تغيير كلمة مرور admin
```bash
python manage.py changepassword admin
```

### جمع Static Files
```bash
python manage.py collectstatic --no-input
```

### إنشاء Backup
```bash
python manage.py dumpdata > backup.json
```

## 🚨 في حالة الطوارئ

1. **تسريب SECRET_KEY:**
   - غير الـ SECRET_KEY فوراً
   - أعد تسجيل دخول جميع المستخدمين
   - فحص logs للنشاطات المشبوهة

2. **هجوم DDoS:**
   - فعّل Rate Limiting
   - استخدم Cloudflare أو AWS Shield
   - حظر IPs المشبوهة

3. **SQL Injection:**
   - Django ORM يحمي تلقائياً
   - لا تستخدم raw SQL إلا بحذر شديد
   - استخدم parameterized queries

4. **XSS Attack:**
   - Django templates تحمي تلقائياً
   - لا تستخدم `|safe` إلا عند الضرورة
   - Sanitize user inputs

## 📞 جهات الاتصال

- فريق الأمن: security@yourdomain.com
- الدعم الفني: support@yourdomain.com
- الطوارئ: +971-XXX-XXXX
