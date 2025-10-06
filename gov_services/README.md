# 🚓 بوابة الخدمات الحكومية - شرطة الشارقة

نظام متكامل لإدارة الخدمات الحكومية والاستعلامات للمواطنين في دولة الإمارات العربية المتحدة.

## 🌟 الميزات الرئيسية

### للمواطنين:
- ✅ تقديم طلبات الخدمات الحكومية
- ✅ الاستعلام عن حالة البلاغات
- ✅ استلام إشعارات بريد إلكتروني تلقائية
- ✅ واجهة عربية سهلة الاستخدام
- ✅ تصميم متجاوب يعمل على جميع الأجهزة

### للموظفين:
- ✅ لوحة تحكم متقدمة لإدارة الطلبات
- ✅ نظام حجز الطلبات لتجنب التضارب
- ✅ إرسال الردود عبر البريد الإلكتروني
- ✅ سجلات تدقيق شاملة (Audit Logs)
- ✅ نظام أمان متقدم

## 🔐 الأمان

- ✅ حماية من هجمات CSRF
- ✅ Rate Limiting لمنع الإساءة
- ✅ تشفير كلمات المرور بـ PBKDF2
- ✅ حماية من Brute Force Attacks
- ✅ Security Headers متقدمة
- ✅ IP Blocking للعناوين المشبوهة
- ✅ Session Security محسّنة

## 🛠️ التقنيات المستخدمة

- **Backend:** Django 5.2.6
- **Database:** SQLite (تطوير) / PostgreSQL (إنتاج)
- **Frontend:** HTML5, CSS3, JavaScript
- **Email:** SMTP (Gmail/Outlook)
- **Deployment:** DigitalOcean App Platform
- **Static Files:** WhiteNoise

## 📦 المتطلبات

```txt
Django==5.2.6
whitenoise==6.6.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9  # للإنتاج فقط
```

## 🚀 التثبيت والتشغيل المحلي

### 1. استنساخ المشروع:
```bash
git clone https://github.com/hamad26650/gov-services-portal.git
cd gov-services-portal/gov_services
```

### 2. إنشاء بيئة افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

### 4. تطبيق Migrations:
```bash
python manage.py migrate
```

### 5. إنشاء حساب مدير:
```bash
python manage.py createsuperuser
```

### 6. تشغيل الخادم:
```bash
python manage.py runserver
```

الموقع سيكون متاحاً على: `http://127.0.0.1:8000`

## 🌐 النشر على DigitalOcean

الموقع منشور حالياً على: **https://octopus-app-glkh4.ondigitalocean.app**

### متغيرات البيئة المطلوبة:
```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=postgresql://...  # يتم إنشاؤه تلقائياً
```

### لإعداد Gmail:
1. فعّل Two-Factor Authentication
2. أنشئ App Password من: https://myaccount.google.com/apppasswords
3. أضف المتغيرات في DigitalOcean Environment Variables

## 📂 هيكل المشروع

```
gov_services/
├── gov_services/          # إعدادات المشروع
│   ├── settings.py       # الإعدادات الرئيسية
│   ├── urls.py          # URLs الرئيسية
│   └── wsgi.py          # WSGI configuration
├── services/            # تطبيق الخدمات
│   ├── models.py       # نماذج البيانات
│   ├── views.py        # Views والمنطق
│   ├── forms.py        # نماذج الإدخال
│   ├── urls.py         # URLs التطبيق
│   ├── admin.py        # لوحة الإدارة
│   ├── middleware.py   # Middleware أمني
│   ├── decorators.py   # Decorators مخصصة
│   ├── templates/      # قوالب HTML
│   ├── static/         # ملفات CSS, JS, Images
│   └── utils/          # خدمات مساعدة
│       └── email_service.py
├── manage.py           # أداة إدارة Django
└── requirements.txt    # المتطلبات
```

## 📧 نظام البريد الإلكتروني

النظام يرسل إيميلات تلقائية في الحالات التالية:

1. **للمواطن:** تأكيد استلام الطلب
2. **للمواطن:** تأكيد استلام الاستعلام
3. **للموظفين:** إشعار باستعلام جديد
4. **للمواطن:** رد من الموظف على الاستعلام

جميع الإيميلات بتصميم HTML جميل ومتجاوب.

## 🔧 الأوامر المفيدة

### إنشاء مستخدم admin:
```bash
python manage.py createsuperuser
```

### جمع الملفات الثابتة:
```bash
python manage.py collectstatic
```

### فحص المشروع:
```bash
python manage.py check
```

### عمل backup للبيانات:
```bash
python manage.py dumpdata > backup.json
```

## 📊 لوحة التحكم

### للمواطنين:
- الصفحة الرئيسية: `/`
- تقديم طلب: `/submit-report/`
- الاستعلام: `/check-report-status/`

### للموظفين:
- تسجيل الدخول: `/staff/login/`
- لوحة التحكم: `/staff/dashboard/`

### للمطورين:
- لوحة الإدارة: `/admin/`

## 🛡️ الأمان

### ميزات الأمان المطبقة:
- ✅ HTTPS إجباري (في الإنتاج)
- ✅ CSRF Protection
- ✅ XSS Protection
- ✅ Clickjacking Protection
- ✅ HSTS Headers
- ✅ Content Security Policy
- ✅ Rate Limiting
- ✅ IP Blocking
- ✅ Session Security
- ✅ Secure Cookies
- ✅ Password Hashing (PBKDF2)
- ✅ Audit Logging

## 📝 الترخيص

هذا المشروع مطور لصالح شرطة الشارقة - دولة الإمارات العربية المتحدة.

## 👥 التواصل

- **الموقع:** https://octopus-app-glkh4.ondigitalocean.app
- **GitHub:** https://github.com/hamad26650/gov-services-portal

---

© 2024 شرطة الشارقة - دولة الإمارات العربية المتحدة. جميع الحقوق محفوظة.

