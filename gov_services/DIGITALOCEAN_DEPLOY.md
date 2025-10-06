# 🚀 دليل النشر على DigitalOcean App Platform

## 📋 الخطوات المطلوبة:

### 1️⃣ إنشاء حساب DigitalOcean

1. اذهب إلى: https://www.digitalocean.com
2. انقر على **Sign Up**
3. سجّل باستخدام:
   - البريد الإلكتروني
   - أو GitHub (أسرع وأسهل)
4. **ستحصل على $200 رصيد مجاني لمدة 60 يوم!** 🎁
5. أضف طريقة دفع (بطاقة ائتمانية/فيزا)

---

### 2️⃣ رفع التعديلات على GitHub

```bash
# تأكد أنك في مجلد المشروع الرئيسي
cd c:\Users\User\OneDrive\Desktop\55

# أضف الملفات الجديدة
git add .

# احفظ التعديلات
git commit -m "Add DigitalOcean configuration"

# ارفع على GitHub
git push origin main
```

---

### 3️⃣ إنشاء التطبيق على DigitalOcean

1. بعد تسجيل الدخول، اذهب إلى: https://cloud.digitalocean.com/apps
2. انقر على **Create App**
3. اختر **GitHub** كمصدر
4. **السماح بالوصول**: اسمح لـ DigitalOcean بالوصول لحساب GitHub الخاص بك
5. اختر المستودع: `hamad26650/gov-services-portal`
6. اختر الفرع: `main`
7. **Auto-deploy**: اترك مفعّل (سيتم النشر تلقائياً عند أي تحديث)
8. انقر **Next**

---

### 4️⃣ إعداد قاعدة البيانات

1. في صفحة الإعداد، سيكتشف DigitalOcean أنك تحتاج PostgreSQL
2. انقر على **Add Database**
3. اختر:
   - **Database Name**: `gov-services-db`
   - **Engine**: PostgreSQL
   - **Version**: 12 أو أحدث
4. انقر **Next**

---

### 5️⃣ ضبط المتغيرات البيئية (Environment Variables)

في صفحة **Environment Variables**، أضف:

```
DJANGO_SECRET_KEY = [اضغط على Generate لتوليد مفتاح عشوائي]
DJANGO_DEBUG = False
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password-here
```

> 📧 **ملاحظة**: استخدم **App Password** من Gmail (ليس كلمة المرور العادية)
> 
> **كيفية الحصول على App Password:**
> 1. اذهب إلى: https://myaccount.google.com/apppasswords
> 2. اختر "Mail" و "Other device"
> 3. انسخ الكلمة المكونة من 16 رقم

---

### 6️⃣ اختيار الخطة

1. في صفحة **Plan**:
   - اختر **Basic**
   - اختر **$5/month** (Basic - 512MB RAM)
2. انقر **Launch App**

---

### 7️⃣ الانتظار (3-5 دقائق)

- ستظهر شاشة Building
- انتظر حتى يصبح الحالة: **Active** ✅
- سيتم إنشاء رابط تلقائي مثل: `https://gov-services-portal-xxxxx.ondigitalocean.app`

---

### 8️⃣ الإعدادات النهائية

بعد نجاح النشر، افتح **Console** (من لوحة التحكم):

```bash
# إنشاء حساب المدير (Admin)
python manage.py create_admin
```

أو يمكنك إنشاء حساب يدوياً:

```bash
python manage.py createsuperuser
```

---

## ✅ تم! المشروع الآن جاهز

### 🔗 الروابط المهمة:

- **الموقع**: سيكون على شكل `https://your-app-name.ondigitalocean.app`
- **لوحة الإدارة**: `https://your-app-name.ondigitalocean.app/admin/`
- **لوحة التحكم**: https://cloud.digitalocean.com/apps

---

## 🔧 إعدادات إضافية (اختيارية)

### إضافة دومين خاص:

1. في لوحة التحكم، اختر **Settings** → **Domains**
2. انقر **Add Domain**
3. أدخل الدومين الخاص بك
4. اتبع التعليمات لإضافة سجلات DNS

### زيادة الموارد:

إذا احتجت أداء أفضل لاحقاً:
- يمكنك الترقية إلى 1GB RAM ($12/شهر)
- أو 2GB RAM ($24/شهر)

---

## 🆘 في حالة وجود مشاكل:

### مشكلة 1: الموقع لا يعمل
```bash
# افتح Logs من لوحة التحكم
# ابحث عن الأخطاء
```

### مشكلة 2: قاعدة البيانات لا تعمل
- تأكد من أن DATABASE_URL موجود في Environment Variables
- تأكد من اتصال Database بالتطبيق

### مشكلة 3: الملفات الثابتة (Static Files) لا تظهر
```bash
# افتح Console وشغّل:
python manage.py collectstatic --noinput
```

---

## 📊 التكلفة الشهرية:

- **App (512MB RAM)**: $5/شهر
- **PostgreSQL Database (1GB)**: مجاني
- **SSL Certificate**: مجاني
- **Bandwidth**: مجاني (1TB)

**المجموع: $5 شهرياً فقط!** 💰

---

## 🎓 نصائح مهمة:

1. ✅ استخدم **App Password** من Gmail (ليس كلمة المرور العادية)
2. ✅ احتفظ بنسخة احتياطية من `DJANGO_SECRET_KEY`
3. ✅ فعّل **Auto-deploy** لتحديث الموقع تلقائياً
4. ✅ راقب الـ Logs بانتظام
5. ✅ اعمل Backup لقاعدة البيانات أسبوعياً

---

## 📞 الدعم:

- **DigitalOcean Docs**: https://docs.digitalocean.com/products/app-platform/
- **Community**: https://www.digitalocean.com/community

---

**تم إعداد هذا الدليل خصيصاً لمشروع gov-services-portal** ✅

