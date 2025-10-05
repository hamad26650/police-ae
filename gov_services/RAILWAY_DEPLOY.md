# 🚂 دليل النشر على Railway.app

## لماذا Railway؟
- ✅ سهل جداً للمبتدئين
- ✅ HTTPS تلقائي مجاني
- ✅ PostgreSQL مجاني
- ✅ Deploy تلقائي من GitHub
- ✅ السعر: 5$ شهرياً (أو مجاني للتجربة)

---

## 📝 خطوات النشر (10 دقائق):

### **الخطوة 1: تجهيز المشروع**

1. **أنشئ ملف `runtime.txt`:**
```bash
cd gov_services
echo python-3.11.0 > runtime.txt
```

2. **أنشئ ملف `Procfile`:**
```bash
echo "web: gunicorn gov_services.wsgi --log-file -" > Procfile
```

3. **حدّث `requirements.txt`:**
```bash
pip install gunicorn psycopg2-binary dj-database-url whitenoise
pip freeze > requirements.txt
```

4. **عدّل `settings.py`:**
أضف في آخر الملف:
```python
import dj_database_url

# Railway Configuration
if 'RAILWAY_ENVIRONMENT' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = ['*']  # سيتم تحديده لاحقاً
    
    # Database from Railway
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
    
    # WhiteNoise for static files
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

---

### **الخطوة 2: رفع على GitHub**

```bash
# إذا ما عندك Git
git init
git add .
git commit -m "Initial commit for Railway deployment"

# أنشئ Repository على GitHub ثم:
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

---

### **الخطوة 3: النشر على Railway**

1. **افتح Railway.app:**
   - اذهب إلى: https://railway.app
   - سجل دخول بـ GitHub

2. **أنشئ مشروع جديد:**
   - اضغط "New Project"
   - اختر "Deploy from GitHub repo"
   - اختر مشروعك `gov_services`

3. **أضف PostgreSQL:**
   - اضغط "+ New"
   - اختر "Database"
   - اختر "PostgreSQL"

4. **اربط Database بالمشروع:**
   - افتح إعدادات المشروع
   - اضغط "Variables"
   - Railway سيضيف `DATABASE_URL` تلقائياً

5. **أضف المتغيرات الإضافية:**
```
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
RAILWAY_ENVIRONMENT=production
```

6. **انتظر Deploy:**
   - Railway سيبني المشروع تلقائياً
   - سيظهر لك URL مثل: `yourproject.up.railway.app`

---

### **الخطوة 4: إعدادات ما بعد النشر**

```bash
# افتح Railway CLI Terminal من الموقع، ثم نفذ:
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 🎉 **جاهز!**

موقعك الآن شغال على:
- ✅ **HTTPS** تلقائي
- ✅ **PostgreSQL** database
- ✅ **Auto-deploy** من GitHub
- ✅ **دومين مجاني** من Railway

---

## 💰 **التكلفة:**

- **خطة Hobby**: 5$ شهرياً
  - 500 ساعة تشغيل شهرياً
  - PostgreSQL مجاني
  - SSL مجاني
  - مناسب تماماً لمشروعك

- **خطة Pro**: 20$ شهرياً
  - تشغيل دائم
  - أداء أعلى

---

## 🔧 **نصائح:**

1. **دومين مخصص (اختياري):**
   - اشتر دومين من Namecheap (12$ سنوياً)
   - اربطه في إعدادات Railway

2. **Backup تلقائي:**
   - Railway يعمل backup تلقائي للـ database

3. **Monitoring:**
   - Railway يوفر logs مباشرة
   - شوف الأخطاء من Dashboard

---

## 📞 **مشاكل شائعة:**

### **المشكلة:** Static files ما تظهر
**الحل:**
```bash
python manage.py collectstatic --noinput
```

### **المشكلة:** Database connection error
**الحل:**
تأكد من `dj-database-url` مثبت في `requirements.txt`

### **المشكلة:** 502 Bad Gateway
**الحل:**
تأكد من `Procfile` صحيح وأن `gunicorn` مثبت

---

## 🚀 **الخلاصة:**

Railway = أسهل طريقة لنشر Django!

**المميزات:**
- ✅ سهل للغاية
- ✅ رخيص (5$ شهرياً)
- ✅ HTTPS مجاني
- ✅ PostgreSQL مجاني
- ✅ Auto-deploy من GitHub
- ✅ Support ممتاز

**مناسب لـ:**
- ✅ مشاريع التخرج
- ✅ Portfolios
- ✅ مواقع صغيرة ومتوسطة
- ✅ MVPs

---

**جربه الحين! 🎯**
https://railway.app
