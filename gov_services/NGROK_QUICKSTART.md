# ⚡ دليل Ngrok السريع

## خطوة 1️⃣: تحميل Ngrok

### لـ Windows:
1. اذهب إلى: https://ngrok.com/download
2. اضغط "Download for Windows"
3. فك الضغط عن الملف في مكان مناسب (مثلاً: `C:\ngrok\`)

---

## خطوة 2️⃣: تشغيل الموقع

```bash
# افتح PowerShell في مجلد المشروع:
cd C:\Users\User\OneDrive\Desktop\55\gov_services
python manage.py runserver 0.0.0.0:8000
```

✅ **خلي هذا الـ terminal مفتوح!**

---

## خطوة 3️⃣: تشغيل Ngrok

### افتح PowerShell **جديد** (terminal ثاني):

```bash
# اذهب لمجلد ngrok:
cd C:\ngrok

# شغل ngrok:
.\ngrok http 8000
```

---

## خطوة 4️⃣: انسخ الرابط! 🎉

**بتشوف شاشة مثل هذي:**

```
ngrok

Session Status                online
Account                       [your email] (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**الرابط الخاص بك هو:**
```
https://abc123.ngrok.io
```

---

## خطوة 5️⃣: تحديث ALLOWED_HOSTS

### افتح `settings.py` وعدّل:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.50.149', 'abc123.ngrok.io', '*']
```

⚠️ **استبدل `abc123.ngrok.io` بالرابط الخاص بك!**

---

## خطوة 6️⃣: شارك الرابط! 🎊

**أرسل الرابط لأي شخص:**
```
https://abc123.ngrok.io
```

✅ يقدر يدخل من أي مكان في العالم!  
✅ يشتغل على الهاتف والكمبيوتر!  
✅ آمن بـ HTTPS!

---

## 🔒 ملاحظات الأمان

### الموقع الآن محمي بـ:
- ✅ Rate Limiting (حد الطلبات)
- ✅ Account Lockout (قفل الحساب)
- ✅ IP Tracking (تتبع IP)
- ✅ Security Headers
- ✅ HTTPS من Ngrok

### تحذيرات:
- ⚠️ **لا تشارك معلومات الدخول (admin/password)**
- ⚠️ **راقب السجلات في `logs/`**
- ⚠️ **الرابط يتغير عند إعادة تشغيل ngrok**

---

## 🎯 نصائح مهمة

### 1. احفظ الرابط:
```
الرابط الحالي: https://abc123.ngrok.io
```

### 2. لو تبا الرابط يبقى ثابت:
- سجّل حساب في ngrok.com
- استخدم Auth Token
- اشترك في خطة مدفوعة (اختياري)

### 3. لو تبا تطفي ngrok:
- اضغط `Ctrl + C` في terminal ngrok
- الموقع يوقف للعامة
- يبقى شغال على جهازك فقط

### 4. لو تبا تشغله مرة ثانية:
```bash
.\ngrok http 8000
```
⚠️ **الرابط بتغير! خذ الرابط الجديد**

---

## 🚨 استكشاف الأخطاء

### المشكلة: "ERR_NGROK_8012"
**الحل:** اقفل ngrok القديم وشغله من جديد

### المشكلة: "Tunnel not found"
**الحل:** تأكد إن Django شغال على port 8000

### المشكلة: "CSRF verification failed"
**الحل:** تأكد إنك ضفت الرابط في ALLOWED_HOSTS

---

## 📊 مراقبة الزوار

### شاهد الزوار في الوقت الفعلي:
```
http://127.0.0.1:4040
```

**بتشوف:**
- ✅ عدد الزوار
- ✅ الطلبات
- ✅ البيانات المرسلة

---

## 🎉 تهانينا!

**الموقع الآن:**
- ✅ شغال للعامة
- ✅ آمن بـ HTTPS
- ✅ محمي من الهجمات
- ✅ جاهز لاستقبال الزوار

---

## 📞 للانتقال للحل الدائم

بعد ما تجرب الموقع وتتأكد إنه شغال:
- راجع `DEPLOY_GUIDE.md`
- انتقل لـ PythonAnywhere (مجاني ودائم)

---

**رابطك الآن:**
```
https://[الرابط-الخاص-بك].ngrok.io
```

**شاركه مع العالم! 🌍✨**
