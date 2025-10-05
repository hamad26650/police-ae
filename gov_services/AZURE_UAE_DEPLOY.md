# 🇦🇪 دليل النشر على Microsoft Azure UAE

## لماذا Azure UAE للمشاريع في الإمارات؟

### ✅ **المميزات الرئيسية:**
1. **Data Centers في الإمارات** (Dubai + Abu Dhabi)
2. **متوافق 100% مع قوانين الإمارات**
3. **سرعة فائقة للمستخدمين المحليين** (<5ms latency)
4. **دعم فني محلي بالعربي**
5. **أمان عالي** (ISO 27001, SOC 1/2/3)
6. **مناسب للمشاريع الحكومية**

---

## 💰 التكلفة التقريبية:

### **للمواقع الصغيرة/المتوسطة:**
- **App Service (Web Hosting):** 50-100 AED/شهر
- **PostgreSQL Database:** 40-80 AED/شهر
- **Storage (Static Files):** 10-20 AED/شهر
- **Domain & SSL:** مجاني مع Azure
- **المجموع:** ~150-250 AED شهرياً

### **للمواقع الكبيرة:**
- 300-500 AED شهرياً

---

## 📝 خطوات النشر (15 دقيقة):

### **الخطوة 1: إنشاء حساب Azure**

1. افتح: https://azure.microsoft.com/ar-ae/
2. اضغط "بدء مجاناً" (تحصل 200$ رصيد مجاني!)
3. سجل بإيميلك (ممكن Gmail)
4. حط بيانات البطاقة (ما راح يخصمون لك لمدة شهر)

---

### **الخطوة 2: تجهيز المشروع**

#### **أ. إنشاء الملفات المطلوبة:**

**1. ملف `requirements.txt`:**
```bash
cd gov_services
pip install gunicorn psycopg2-binary dj-database-url whitenoise
pip freeze > requirements.txt
```

**2. ملف `startup.sh`:**
```bash
#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn gov_services.wsgi --bind=0.0.0.0:8000 --timeout 600
```

اجعله قابل للتنفيذ:
```bash
chmod +x startup.sh
```

**3. عدّل `settings.py`:**
أضف في آخر الملف:
```python
import dj_database_url

# Azure Configuration
if 'WEBSITE_HOSTNAME' in os.environ:  # Azure environment
    DEBUG = False
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
    
    # Database from Azure PostgreSQL
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
    
    # WhiteNoise for static files
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Security Settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

### **الخطوة 3: رفع على GitHub**

```bash
git init
git add .
git commit -m "Ready for Azure deployment"

# أنشئ repository على GitHub ثم:
git remote add origin YOUR_GITHUB_URL
git branch -M main
git push -u origin main
```

---

### **الخطوة 4: إنشاء الموارد على Azure**

#### **أ. إنشاء Resource Group:**
```bash
# افتح Azure Portal: https://portal.azure.com
# اختر المنطقة: "UAE North" (Dubai) أو "UAE Central" (Abu Dhabi)
```

**من Azure Portal:**
1. اضغط "Create a resource"
2. ابحث عن "Resource Group"
3. اسم المجموعة: `gov-services-rg`
4. **المنطقة: UAE North (Dubai)** ⭐ مهم!
5. Review + Create

#### **ب. إنشاء PostgreSQL Database:**

1. اضغط "Create a resource"
2. ابحث عن "Azure Database for PostgreSQL"
3. اختر "Flexible Server"
4. الإعدادات:
   - **Server name:** `gov-services-db`
   - **المنطقة: UAE North** ⭐
   - **Version:** 14
   - **Compute + Storage:** Burstable, B1ms (أرخص - مناسب للبداية)
   - **Username:** `dbadmin`
   - **Password:** اختر كلمة سر قوية
5. Networking:
   - اختر "Allow public access from any Azure service"
6. Create

**احفظ Connection String:**
```
postgresql://dbadmin:YOUR_PASSWORD@gov-services-db.postgres.database.azure.com:5432/postgres?sslmode=require
```

#### **ج. إنشاء Web App:**

1. اضغط "Create a resource"
2. ابحث عن "Web App"
3. الإعدادات:
   - **Name:** `gov-services-uae` (سيصبح: gov-services-uae.azurewebsites.net)
   - **Publish:** Code
   - **Runtime:** Python 3.11
   - **المنطقة: UAE North** ⭐⭐⭐
   - **Plan:** Basic B1 (~50 AED/شهر)
4. Create

---

### **الخطوة 5: ربط GitHub بـ Azure**

**من Web App:**
1. افتح Web App اللي أنشأته
2. من القائمة اليسار: "Deployment Center"
3. Source: **GitHub**
4. سجل دخول GitHub
5. اختر:
   - Organization: حسابك
   - Repository: `gov_services`
   - Branch: `main`
6. Save

**Azure سيبني المشروع تلقائياً!** 🚀

---

### **الخطوة 6: إضافة المتغيرات البيئية**

**من Web App → Configuration → Application Settings:**

أضف:
```
DJANGO_SECRET_KEY = your-super-secret-key-here
DJANGO_DEBUG = False
DATABASE_URL = postgresql://dbadmin:PASSWORD@gov-services-db.postgres.database.azure.com:5432/postgres?sslmode=require
WEBSITE_HOSTNAME = gov-services-uae.azurewebsites.net
```

احفظ وأعد التشغيل.

---

### **الخطوة 7: تشغيل الأوامر الأولية**

**من Azure Portal → Web App → SSH:**

```bash
cd /home/site/wwwroot
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 🎉 **جاهز!**

موقعك الآن شغال على:
```
https://gov-services-uae.azurewebsites.net
```

### ✅ **المميزات:**
- 🇦🇪 مستضاف في **دبي، الإمارات**
- 🔒 **HTTPS** تلقائي مجاني
- ⚡ **سريع جداً** للمستخدمين المحليين
- 🛡️ **آمن** ومتوافق مع القوانين
- 📊 **Monitoring** مدمج
- 💾 **Backup** تلقائي

---

## 🌐 **إضافة دومين مخصص (اختياري):**

### **مثال: police.ae**

1. **اشتر دومين من:**
   - ae.godaddy.com (للدومينات .ae)
   - namecheap.com (للدومينات .com)

2. **من Azure Web App → Custom Domains:**
   - اضغط "Add custom domain"
   - ادخل: `police.ae` أو `www.police.ae`
   - اتبع التعليمات لإضافة DNS Records

3. **SSL مجاني:**
   - Azure يوفر SSL مجاني للدومينات المخصصة
   - يتجدد تلقائياً

---

## 📊 **Monitoring والإحصائيات:**

**Azure يوفر:**
- ✅ **Application Insights:** لمراقبة الأداء
- ✅ **Log Stream:** لمتابعة الأخطاء مباشرة
- ✅ **Metrics:** CPU, Memory, Requests
- ✅ **Alerts:** إشعارات عند وجود مشاكل

**للتفعيل:**
Web App → Monitoring → Application Insights → Enable

---

## 💡 **نصائح للتوفير:**

### **1. استخدم Azure Free Credits:**
- 200$ مجاناً لأول شهر
- يكفي للتجربة والتطوير

### **2. اختر الباقة المناسبة:**
- **Dev/Test:** B1 (50 AED/شهر) - للتطوير
- **Production:** S1 (150 AED/شهر) - للإنتاج
- **Enterprise:** P1V2 (300+ AED/شهر) - للمواقع الكبيرة

### **3. أطفئ البيئات التطويرية:**
- أطفئ الموارد اللي ما تستخدمها
- وفر 70% من التكلفة

---

## 🔧 **مشاكل شائعة:**

### **المشكلة: Static files ما تظهر**
**الحل:**
```bash
python manage.py collectstatic --noinput
# تأكد من WhiteNoise في settings.py
```

### **المشكلة: Database connection error**
**الحل:**
- تأكد من `DATABASE_URL` صحيح في Configuration
- تأكد من Firewall Rules في PostgreSQL

### **المشكلة: 500 Internal Server Error**
**الحل:**
```bash
# شوف اللوجات:
Web App → Log Stream
```

---

## 📞 **الدعم الفني:**

### **Azure Support في الإمارات:**
- 📧 Email: azure-support@microsoft.com
- 📱 هاتف: 800-1444 (مجاني داخل الإمارات)
- 💬 Chat: من Azure Portal
- 🌐 الموقع: https://azure.microsoft.com/ar-ae/support/

### **المجتمع:**
- Stack Overflow
- Azure Community Forums
- Microsoft Docs

---

## 🎓 **موارد إضافية:**

1. **Azure Learning Path (بالعربي):**
   https://docs.microsoft.com/ar-ae/learn/azure/

2. **Azure Pricing Calculator:**
   https://azure.microsoft.com/en-us/pricing/calculator/

3. **Django on Azure Tutorial:**
   https://docs.microsoft.com/en-us/azure/app-service/quickstart-python

---

## 🏆 **الخلاصة:**

### **Azure UAE مناسب لك لأن:**

✅ **قانوني:** متوافق 100% مع قوانين الإمارات  
✅ **سريع:** Data centers في دبي  
✅ **آمن:** أعلى معايير الأمان  
✅ **موثوق:** 99.95% uptime SLA  
✅ **احترافي:** يناسب المشاريع الحكومية  
✅ **دعم محلي:** فريق دعم في الإمارات  

---

## 💰 **التكلفة الإجمالية المتوقعة:**

### **للبداية (3-6 أشهر):**
- 🎁 **مجاني** باستخدام Azure Free Credits!

### **بعد انتهاء الفترة المجانية:**
- 💰 **~150-250 AED/شهر** للمواقع الصغيرة
- 💰 **~300-500 AED/شهر** للمواقع المتوسطة

**مقارنة بالبدائل:**
- أرخص من AWS بـ 20-30%
- أغلى من DigitalOcean بـ 2-3x لكن أفضل بكثير!

---

## 🚀 **ابدأ الآن:**

1. سجل في Azure: https://azure.microsoft.com/ar-ae/
2. احصل على 200$ مجاناً
3. اتبع الدليل أعلاه
4. موقعك شغال في الإمارات خلال 15 دقيقة!

---

**بالتوفيق! 🇦🇪✨**
