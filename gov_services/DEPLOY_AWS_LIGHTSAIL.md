# 🚀 دليل النشر على AWS Lightsail (البحرين)

## ⏱️ الوقت المتوقع: 15-20 دقيقة

---

## 📋 المتطلبات قبل البدء:

- ✅ حساب AWS (سنشرح كيف تسويه)
- ✅ بطاقة ائتمانية (للتحقق فقط)
- ✅ معلومات Gmail (للإيميلات)

---

## 🔗 الخطوة 1: التسجيل في AWS

### 1. اذهب إلى:
👉 https://aws.amazon.com/lightsail/

### 2. اضغط "Get started for free" أو "Sign up"

### 3. أدخل معلوماتك:
- البريد الإلكتروني
- كلمة مرور قوية
- اسم الحساب (مثلاً: Police Portal)

### 4. معلومات الاتصال:
- نوع الحساب: Personal أو Business
- الاسم الكامل
- رقم الجوال
- العنوان

### 5. معلومات الدفع:
- ⚠️ **مهم:** البطاقة للتحقق فقط
- لن يتم الخصم إلا عند الاستخدام
- السعر: $5/شهر فقط

### 6. التحقق من الهوية:
- سيرسلون كود على جوالك
- أدخل الكود

### 7. اختر الخطة:
- اختر **Basic Support** (مجاني)

### 8. تم! 🎉

---

## 🖥️ الخطوة 2: إنشاء Instance

### 1. اذهب إلى Lightsail Console:
👉 https://lightsail.aws.amazon.com/

### 2. اضغط "Create instance" (برتقالي)

### 3. اختر المنطقة (Region):
- **اختر:** Middle East (Bahrain) 🇧🇭
- أو: Asia Pacific (Mumbai) 🇮🇳
- **مهم:** اختر الأقرب لك!

### 4. اختر Platform:
- اختر: **Linux/Unix**

### 5. اختر Blueprint:
- اختر: **OS Only**
- اختر: **Ubuntu 22.04 LTS**

### 6. اختر الخطة (Plan):

**موصى به:** 💰 **$5/شهر**
```
- 1 GB RAM
- 1 Core CPU
- 40 GB SSD
- 2 TB Transfer
```

**إذا تتوقع زيارات كثيرة:** 💰 **$10/شهر**
```
- 2 GB RAM
- 1 Core CPU
- 60 GB SSD
- 3 TB Transfer
```

### 7. اسم Instance:
- اكتب: `police-portal` أو أي اسم تحبه

### 8. اضغط "Create instance" (برتقالي)

### 9. انتظر 1-2 دقيقة ⏰

لما يصير الـ Status: **Running** 🟢، يعني جاهز!

---

## 🔐 الخطوة 3: الاتصال بالسيرفر

### طريقة 1: من Browser (الأسهل)

1. في Lightsail Console، اضغط على Instance
2. اضغط "Connect using SSH" (من الأعلى)
3. راح ينفتح Terminal في المتصفح
4. ✅ جاهز للاستخدام!

### طريقة 2: من جهازك (للمحترفين)

1. حمّل SSH Key من AWS
2. استخدم PuTTY (Windows) أو Terminal (Mac/Linux)

---

## 🚀 الخطوة 4: تثبيت المشروع

### في الـ Terminal (اللي فتحته فوق)، اكتب هذي الأوامر:

### 1️⃣ تحميل المشروع من GitHub:

```bash
cd /home/ubuntu
git clone https://github.com/hamad26650/police-ae.git police-portal
cd police-portal/gov_services
```

### 2️⃣ تشغيل سكريبت النشر التلقائي:

```bash
chmod +x deploy_aws.sh
sudo ./deploy_aws.sh
```

⏰ **انتظر 5-10 دقائق** - السكريبت راح يسوي كل شي تلقائياً:
- ✅ تثبيت Python, PostgreSQL, Nginx
- ✅ إنشاء قاعدة البيانات
- ✅ تثبيت المشروع
- ✅ إعداد Gunicorn
- ✅ إعداد Nginx
- ✅ كل شي! 🎉

### 3️⃣ **احفظ كلمة مرور قاعدة البيانات!**

في نهاية السكريبت، راح يعطيك معلومات مهمة:
```
كلمة المرور: ABC123XYZ456...
```

📝 **احفظها في مكان آمن!**

---

## ⚙️ الخطوة 5: إعدادات Gmail

### 1. عدّل ملف .env:

```bash
cd /home/ubuntu/police-portal/gov_services
nano .env
```

### 2. أضف معلومات Gmail:

غيّر هذي السطور:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
```

حط معلوماتك:
```env
EMAIL_HOST_USER=hamad@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

### 3. احفظ الملف:
- اضغط `Ctrl + O` (حفظ)
- اضغط `Enter`
- اضغط `Ctrl + X` (خروج)

### 4. أعد تشغيل Gunicorn:

```bash
sudo systemctl restart gunicorn
```

---

## 👤 الخطوة 6: إنشاء مستخدم Admin

```bash
cd /home/ubuntu/police-portal/gov_services
source /home/ubuntu/police-portal/venv/bin/activate
python manage.py createsuperuser
```

أدخل:
- اسم المستخدم (مثلاً: admin)
- البريد الإلكتروني
- كلمة المرور (قوية!)

---

## 🌐 الخطوة 7: الحصول على IP والوصول للموقع

### 1. احصل على Public IP:

في Lightsail Console:
- اضغط على Instance
- لاحظ **Public IP** مثلاً: `15.185.123.45`

### 2. افتح المتصفح:

```
http://15.185.123.45
```

### 🎉 مبروك! موقعك شغّال!

---

## 🔒 الخطوة 8: إعداد Domain واسم نطاق (اختياري)

### إذا عندك Domain:

1. في Lightsail Console:
   - اذهب إلى "Networking"
   - اضغط "Create static IP"
   - ربطه بالـ Instance

2. في مزود الدومين (مثل Namecheap):
   - أضف A Record يشير للـ Static IP

3. عدّل ملف .env:
```bash
nano /home/ubuntu/police-portal/gov_services/.env
```

غيّر:
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

4. أعد التشغيل:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 🔐 الخطوة 9: إضافة SSL (HTTPS) - موصى به!

### استخدام Let's Encrypt (مجاني):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

اتبع التعليمات وتم! 🔒

---

## 🔧 أوامر مفيدة للصيانة:

### إعادة تشغيل الخدمات:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### عرض logs:
```bash
# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### تحديث المشروع من GitHub:
```bash
cd /home/ubuntu/police-portal
git pull origin main
source venv/bin/activate
cd gov_services
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## 📊 معلومات الأسعار:

| الخطة | RAM | CPU | Storage | السعر |
|-------|-----|-----|---------|-------|
| 512MB | 512MB | 1 | 20GB | $3.50 |
| 1GB | 1GB | 1 | 40GB | $5 ⭐ |
| 2GB | 2GB | 1 | 60GB | $10 |

⭐ **موصى به للبداية**

---

## ❓ حل المشاكل:

### المشكلة: الموقع ما يفتح

**الحل:**
```bash
# تحقق من الخدمات
sudo systemctl status gunicorn
sudo systemctl status nginx

# أعد التشغيل
sudo systemctl restart gunicorn nginx
```

### المشكلة: خطأ 502 Bad Gateway

**الحل:**
```bash
# تحقق من logs
sudo journalctl -u gunicorn -n 50

# غالباً مشكلة في الكود
cd /home/ubuntu/police-portal/gov_services
source /home/ubuntu/police-portal/venv/bin/activate
python manage.py check
```

### المشكلة: Gmail ما يشتغل

**الحل:**
1. تأكد من App Password صحيح
2. تأكد من التحقق بخطوتين مفعّل
3. تحقق من ملف .env

---

## 📞 الدعم:

- **AWS Support:** https://console.aws.amazon.com/support/
- **GitHub Issues:** https://github.com/hamad26650/police-ae/issues

---

## ✅ Checklist النشر:

- [ ] تم إنشاء حساب AWS
- [ ] تم إنشاء Instance في البحرين
- [ ] تم تشغيل سكريبت النشر
- [ ] تم حفظ كلمة مرور قاعدة البيانات
- [ ] تم إضافة معلومات Gmail
- [ ] تم إنشاء مستخدم admin
- [ ] الموقع يعمل على IP العام
- [ ] (اختياري) تم ربط الدومين
- [ ] (اختياري) تم تفعيل SSL

---

🎉 **مبروك! موقعك الحين على AWS Lightsail في البحرين!**

السرعة ممتازة للمستخدمين في الخليج! 🚀

