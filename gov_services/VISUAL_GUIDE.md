# 📸 دليل مصوّر - خطوة بخطوة

## 🎯 الهدف: إصلاح مشكلة عدم إرسال الإيميلات

---

## 📍 الخطوة 1: Google App Password

### أ) روح: https://myaccount.google.com/security

```
Google Account
├── Security
    ├── Signing in to Google
    │   └── 2-Step Verification ← فعّل هذا أولاً
    └── App passwords ← بعدها روح هنا
```

### ب) فعّل 2-Step Verification:

```
2-Step Verification
[Get Started] ← اضغط هنا
→ أدخل رقم جوالك
→ استقبل الكود
→ تأكيد
```

### ج) أنشئ App Password:

```
App passwords
[Select app: Other (Custom name)]
Name: Police Portal
[Generate] ← اضغط

النتيجة:
┌─────────────────────────────┐
│  Your app password:         │
│  aaaa bbbb cccc dddd       │
│                             │
│  [Copy to clipboard]        │
└─────────────────────────────┘

⚠️ احذف الـ spaces:
✅ الصحيح: aaaabbbbccccdddd
❌ الغلط: aaaa bbbb cccc dddd
```

---

## 📍 الخطوة 2: DigitalOcean Variables

### أ) روح: https://cloud.digitalocean.com/apps

```
Apps
└── police-portal ← اختر هذا
    └── Settings ← اضغط
        └── Environment Variables ← اضغط
```

### ب) أضف أو عدّل المتغيرات:

```
Environment Variables
┌────────────────────────────────────────┐
│ Key: EMAIL_HOST_USER                   │
│ Value: your-email@gmail.com            │
│ Type: ☑ Secret                         │
│ Scope: ☑ RUN_AND_BUILD_TIME ← مهم!    │
│                                        │
│ [Save]                                 │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ Key: EMAIL_HOST_PASSWORD               │
│ Value: aaaabbbbccccdddd (16 حرف)      │
│ Type: ☑ Secret                         │
│ Scope: ☑ RUN_AND_BUILD_TIME ← مهم!    │
│                                        │
│ [Save]                                 │
└────────────────────────────────────────┘
```

### ج) أعد تشغيل التطبيق:

```
police-portal
[Actions ▼]
  ├── Restart ← اضغط هنا
  ├── ...
  └── ...

⏳ انتظر 2-3 دقائق...

✅ Status: Live
```

---

## 📍 الخطوة 3: الاختبار في Console

### أ) افتح Console:

```
police-portal
[Console] ← اضغط هنا

نافذة الـ Terminal راح تفتح:
┌────────────────────────────────────────┐
│ root@police-portal:~#                  │
│                                        │
└────────────────────────────────────────┘
```

### ب) شغّل الأمر:

```bash
python TEST_EMAIL_REAL.py
```

### ج) النتائج:

#### ✅ إذا نجح:
```
════════════════════════════════════════
🧪 اختبار حقيقي لإرسال الإيميل
════════════════════════════════════════

📋 1️⃣ فحص إعدادات Gmail:
✅ EMAIL_HOST_USER: your-email@gmail.com
✅ EMAIL_HOST_PASSWORD: موجود (16 حرف)

📋 2️⃣ فحص الاستعلامات:
✅ عدد الاستعلامات: 5

🧪 3️⃣ اختبار الإرسال:
⏳ جاري الإرسال...

════════════════════════════════════════
✅ نجح الإرسال!
════════════════════════════════════════

✉️  تم إرسال إيميل إلى: customer@example.com
📨 الرسالة: تم إرسال الرد والبريد الإلكتروني بنجاح

💡 تحقق من صندوق الوارد
✅ إذا وصل الإيميل، معناها النظام يعمل!
```

**🎉 يعني: كل شي تمام!**

---

#### ❌ إذا فشل:
```
════════════════════════════════════════
❌ الإعدادات غير موجودة!
════════════════════════════════════════

💡 الحل:
   1. روح DigitalOcean → Settings → Environment Variables
   2. أضف EMAIL_HOST_USER و EMAIL_HOST_PASSWORD
   3. Scope = RUN_AND_BUILD_TIME
   4. احفظ → Restart → انتظر 3 دقائق
```

**🔧 يعني: ارجع للخطوة 2**

---

## 📍 الخطوة 4: الاختبار من Dashboard

### أ) افتح Dashboard:

```
🌐 https://buhairah-oqh9h.ondigitalocean.app/staff/login/

┌─────────────────────────────────────┐
│  تسجيل دخول الموظفين               │
│                                     │
│  اسم المستخدم: [12345          ]  │
│  كلمة المرور:  [12345          ]  │
│                                     │
│  [تسجيل الدخول]                    │
└─────────────────────────────────────┘
```

### ب) اختر استعلام:

```
Dashboard
┌───────────────────────────────────────────────────────┐
│ ID  │ المركز  │ رقم البلاغ │ البريد الإلكتروني    │
├─────┼─────────┼────────────┼─────────────────────────┤
│ 123 │ البحيرة │ 456/2025   │ customer@example.com   │
│     │         │            │ [عرض]                  │ ← اضغط
└───────────────────────────────────────────────────────┘
```

### ج) اكتب الرد:

```
┌─────────────────────────────────────┐
│  الرد على الاستعلام                │
│                                     │
│  [تم التحقق من البلاغ وهو قيد     │
│   المعالجة. شكراً لتواصلكم.    ]  │
│                                     │
│  [إرسال الرد]                      │ ← اضغط
└─────────────────────────────────────┘
```

### د) النتيجة:

```
✅ تم إرسال الرد بنجاح!
📧 تم إرسال البريد الإلكتروني للمتعامل
```

### هـ) تحقق من بريد المتعامل:

```
customer@example.com - Inbox
┌─────────────────────────────────────┐
│ 📧 رد على استعلامكم - مركز شرطة    │
│    البحيرة                          │
│                                     │
│ تم التحقق من البلاغ وهو قيد       │
│ المعالجة. شكراً لتواصلكم.         │
│                                     │
│ مع تحياتنا،                        │
│ مركز شرطة البحيرة                  │
└─────────────────────────────────────┘
```

**🎉 وصل الإيميل = النظام يعمل!**

---

## 🔍 إذا لازالت المشكلة موجودة:

### تحقق من الإيميل في قاعدة البيانات:

```bash
python manage.py shell
```

```python
>>> from services.models import Inquiry
>>> inquiries = Inquiry.objects.all()
>>> for inq in inquiries:
...     print(f"ID: {inq.id}")
...     print(f"Email: {inq.email}")
...     print(f"Phone: {inq.phone}")
...     print("---")

النتيجة:
ID: 123
Email: 
Phone: 0501234567  ← ❌ هذا رقم هاتف مو إيميل!
---
```

**المشكلة:** المتعامل أدخل رقم هاتف!

**الحل:**
1. قدم استعلام جديد
2. أدخل إيميل صحيح: `test@gmail.com`
3. جرّب مرة ثانية

---

## ✅ Checklist النهائي:

```
☐ 1. Google: فعلت 2-Step Verification
☐ 2. Google: حصلت على App Password (16 حرف)
☐ 3. DigitalOcean: أضفت EMAIL_HOST_USER
☐ 4. DigitalOcean: أضفت EMAIL_HOST_PASSWORD
☐ 5. DigitalOcean: Scope = RUN_AND_BUILD_TIME
☐ 6. DigitalOcean: عملت Restart
☐ 7. انتظرت 3 دقائق
☐ 8. Console: شغلت python TEST_EMAIL_REAL.py
☐ 9. Console: نجح الاختبار ✅
☐ 10. Dashboard: جربت الرد
☐ 11. ✅ وصل الإيميل للمتعامل!
```

---

## 🎯 الخلاصة:

**إذا اتبعت الـ 11 خطوة بالضبط:**
- ✅ راح يشتغل 100%!

**إذا لازالت المشكلة:**
- شغّل `python TEST_EMAIL_REAL.py`
- اقرأ الرسالة بعناية
- السكريبت راح يحدد المشكلة بالضبط

**✅ مضمون!** 🎉

