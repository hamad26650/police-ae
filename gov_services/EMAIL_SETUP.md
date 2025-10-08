# 📧 دليل إعداد الإيميل (Gmail SMTP)

## الخطوات:

### 1️⃣ إنشاء App Password في Gmail

1. افتح: https://myaccount.google.com/security
2. فعّل **2-Step Verification** (إذا مو مفعّل)
3. اذهب إلى **App Passwords**
4. أنشئ App Password جديد:
   - App: **Mail**
   - Device: **Other** → "Police Portal"
5. احفظ الـ 16 حرف (بدون spaces)

---

### 2️⃣ إضافة المتغيرات في DigitalOcean

**في DigitalOcean:**
```
Apps → buhairah → Settings → App-Level Environment Variables
```

**أضف:**

**المتغير 1:**
- Key: `EMAIL_HOST_USER`
- Value: `your-email@gmail.com`
- Encrypt: ✅

**المتغير 2:**
- Key: `EMAIL_HOST_PASSWORD`
- Value: `[App Password من Gmail]`
- Encrypt: ✅

**اضغط Save**

---

### 3️⃣ التحقق (في Console)

```bash
python manage.py shell
```

```python
from django.conf import settings
print(f"HOST: {settings.EMAIL_HOST_USER}")
print(f"PASS: {'✅' if settings.EMAIL_HOST_PASSWORD else '❌'}")
```

---

### 4️⃣ اختبار الإرسال

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test',
    settings.EMAIL_HOST_USER,
    ['test@example.com'],
    fail_silently=False,
)
```

---

## ✅ التحقق من عمل الإيميلات:

1. ✅ سجل دخول كموظف
2. ✅ افتح استعلام جديد
3. ✅ اكتب رد
4. ✅ اضغط "إرسال"
5. ✅ تحقق من إيميل المتعامل

---

## ❗ الأخطاء الشائعة:

### خطأ المصادقة:
```
SMTPAuthenticationError (535)
```
**الحل:** تأكد من App Password صحيح

### Timeout:
```
socket.timeout
```
**الحل:** الكود يتعامل معه تلقائياً

### الإيميل لا يصل:
**السبب:** إيميل المتعامل غلط في الاستعلام
**الحل:** تحقق من حقل "البريد الإلكتروني"

---

## 📊 إحصائيات Gmail:

- 📧 **الحد اليومي:** 500 إيميل
- 📧 **الحد الساعة:** 100 إيميل
- ⏱️ **Timeout:** 10 ثواني

---

## 💡 نصائح:

1. ✅ استخدم Gmail حقيقي (مو تجريبي)
2. ✅ فعّل 2-Step Verification
3. ✅ احفظ App Password في مكان آمن
4. ✅ اختبر الإرسال بعد الإعداد
5. ✅ تحقق من Spam folder في البداية

---

## 🔗 روابط مفيدة:

- Google Account Security: https://myaccount.google.com/security
- App Passwords: https://myaccount.google.com/apppasswords
- Gmail SMTP Settings: https://support.google.com/mail/answer/7126229

---

## 📞 الدعم:

إذا واجهت مشاكل:
1. تحقق من Console logs في DigitalOcean
2. راجع `logs/django.log`
3. شغّل الاختبار في shell

