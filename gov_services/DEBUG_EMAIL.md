# 🐛 تشخيص مشاكل البريد الإلكتروني

## ✅ الخطوات الأساسية

### **1. تأكد من المتغيرات في Railway**

في Railway Dashboard → Variables، يجب أن تكون موجودة:

```
EMAIL_HOST_USER=albuhairah.test@outlook.com
EMAIL_HOST_PASSWORD=H@mad.95335
DEFAULT_FROM_EMAIL=albuhairah.test@outlook.com
```

### **2. تفقد Railway Logs**

في Railway Dashboard → Deployments → View Logs

**ابحث عن:**

#### **✅ نجح:**
```
تم إرسال بريد إلكتروني للاستعلام INQ-000001 إلى albuhairah.test@outlook.com
```

#### **❌ فشل - متغيرات مفقودة:**
```
SMTPSenderRefused: (530, b'5.7.0 Must issue a STARTTLS command first')
```
**الحل:** أضف المتغيرات في Railway

#### **❌ فشل - باسورد خطأ:**
```
SMTPAuthenticationError: (535, b'5.7.3 Authentication unsuccessful')
```
**الحل:** تأكد من الباسورد صحيح

#### **❌ فشل - يحتاج App Password:**
```
SMTPAuthenticationError: (535, b'5.7.139 Authentication unsuccessful')
```
**الحل:** استخدم App Password بدلاً من الباسورد العادي

---

## 🔐 إنشاء App Password لـ Outlook

### **إذا عندك التحقق بخطوتين مفعل:**

**1. اذهب إلى:**
```
https://account.microsoft.com/security
```

**2. اضغط:**
- `Advanced security options`
- `App passwords`
- `+ Create a new app password`

**3. انسخ الباسورد الجديد**
مثال: `abcd-efgh-ijkl-mnop`

**4. استخدمه في Railway:**
```
EMAIL_HOST_PASSWORD=abcd-efgh-ijkl-mnop
```

---

## 🧪 اختبار محلي

### **لاختبار الإيميل على جهازك:**

**1. افتح Terminal في مجلد المشروع:**
```bash
cd gov_services
python manage.py shell
```

**2. جرب إرسال إيميل:**
```python
from django.core.mail import send_mail

send_mail(
    'اختبار',
    'هذا إيميل تجريبي',
    'albuhairah.test@outlook.com',
    ['your-test-email@example.com'],
    fail_silently=False,
)
```

**3. النتيجة:**
- ✅ إذا نجح: `1`
- ❌ إذا فشل: رسالة خطأ توضح المشكلة

---

## 📋 Checklist

### **قبل ما تطلب المساعدة، تأكد من:**

- [ ] المتغيرات الثلاثة مضافة في Railway
- [ ] الباسورد صحيح (بدون فراغات زائدة)
- [ ] Railway أعاد النشر بعد إضافة المتغيرات
- [ ] الإيميل `albuhairah.test@outlook.com` يعمل (جرب تدخل عليه)
- [ ] تفقدت مجلد Spam/Junk في الإيميل

---

## 🔍 أخطاء شائعة

### **1. المتغيرات بفراغات زائدة**
❌ `EMAIL_HOST_USER= albuhairah.test@outlook.com ` (فيه فراغات)
✅ `EMAIL_HOST_USER=albuhairah.test@outlook.com` (بدون فراغات)

### **2. نسيت إعادة النشر**
بعد إضافة المتغيرات، Railway لازم يعيد النشر.
انتظر 1-2 دقيقة بعد الإضافة.

### **3. الإيميل في Spam**
تفقد مجلد Spam/Junk في بريدك.

### **4. Outlook يطلب App Password**
بعض الحسابات تحتاج App Password بدلاً من الباسورد العادي.

---

## 💡 نصائح

### **للاختبار السريع:**
- استخدم إيميلك الشخصي كمُرسل
- أرسل لنفسك للتأكد من الاستلام
- تفقد Railway Logs بعد كل محاولة

### **للإنتاج:**
- استخدم إيميل رسمي للمؤسسة
- فعّل التحقق بخطوتين
- استخدم App Password

---

## 🆘 طلب المساعدة

### **إذا جربت كل شي وما اشتغل:**

**أرسل:**
1. **Screenshot من Railway Variables** (خفي الباسورد!)
2. **آخر 20 سطر من Railway Logs**
3. **الخطأ اللي يطلع** (إذا في)

---

© 2025 - دليل تشخيص البريد الإلكتروني

