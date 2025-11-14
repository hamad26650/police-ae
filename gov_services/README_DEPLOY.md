# 🚀 دليل النشر السريع

## للمطورين: خطوات سريعة للنشر

### 1️⃣ إعداد متغيرات البيئة

أنشئ ملف `.env` في مجلد `gov_services`:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://user:password@localhost:5432/dbname

EMAIL_HOST_USER=Project.test85@outlook.com
EMAIL_HOST_PASSWORD=your-app-password-here
```

### 2️⃣ تشغيل سكريبت النشر

```bash
chmod +x deploy_quick.sh
./deploy_quick.sh
```

### 3️⃣ إعداد قاعدة البيانات

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4️⃣ تشغيل الموقع

```bash
# للتطوير
python manage.py runserver

# للإنتاج
gunicorn gov_services.wsgi:application --config gunicorn_config.py
```

---

## 📋 قائمة التحقق قبل النشر

- [ ] تحديث `ALLOWED_HOSTS` في `.env`
- [ ] تعيين `DJANGO_DEBUG=False`
- [ ] إعداد قاعدة بيانات PostgreSQL
- [ ] إعداد متغيرات البريد الإلكتروني
- [ ] تشغيل `collectstatic`
- [ ] تشغيل migrations
- [ ] إنشاء مستخدم admin
- [ ] اختبار الموقع محلياً
- [ ] إعداد SSL/HTTPS
- [ ] إعداد Nginx (اختياري)
- [ ] إعداد Gunicorn service (اختياري)

---

## 🔧 إعدادات مهمة

### تحديث إيميلات البنوك

عدّل ملف `services/utils/email_service.py`:

```python
BANK_EMAILS = {
    'بنك ابوظبي التجاري': 'adcb@bank.ae',
    'مصرف ابوظبي الاسلامي': 'adib@bank.ae',
    'بنك دبي الاسلامي': 'dib@bank.ae',
}
```

### تحديث إيميلات المراكز

استخدم Django Admin أو قم بتحديثها مباشرة في قاعدة البيانات.

---

## 📞 الدعم

للمزيد من التفاصيل، راجع ملف `DEPLOY.md`

