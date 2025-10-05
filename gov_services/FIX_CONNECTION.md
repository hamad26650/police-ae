# 🔥 حل مشكلة ERR_CONNECTION_RESET

## المشكلة:
Windows Firewall يحجب الاتصالات الخارجية!

---

## ✅ الحل السريع (دقيقتين):

### الطريقة 1: السماح لـ Python في Firewall

#### الخطوات:
1. افتح **Windows Defender Firewall**
   - اضغط `Win + R`
   - اكتب: `firewall.cpl`
   - اضغط Enter

2. من الجهة اليسار، اختر:
   - **Allow an app or feature through Windows Defender Firewall**

3. اضغط **Change settings** (في الأعلى)

4. اضغط **Allow another app...**

5. اضغط **Browse...**

6. اذهب إلى:
   ```
   C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe
   ```

7. اختر **python.exe** واضغط **Add**

8. ✅ تأكد إن Python مفعّل لـ **Private** و **Public**

9. اضغط **OK**

---

### الطريقة 2: فتح Port 8000 مباشرة

#### في PowerShell (كـ Administrator):
```powershell
# السماح بالاتصالات الداخلة على port 8000
netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow protocol=TCP localport=8000
```

---

## ✅ بعد تطبيق الحل:

1. أعد تشغيل السيرفر:
```bash
cd c:\Users\User\OneDrive\Desktop\55\gov_services
python manage.py runserver 0.0.0.0:8000
```

2. جرّب الدخول من جهاز آخر:
```
http://192.168.50.149:8000
```

---

## 🌐 للنشر العام (بدون تعقيدات):

### استخدم Ngrok (الأسهل):
1. حمّل من: https://ngrok.com/download
2. شغّل: `ngrok http 8000`
3. خذ الرابط العام: `https://abc123.ngrok.io`

**مميزات Ngrok:**
- ✅ يتجاوز Firewall تماماً
- ✅ HTTPS تلقائي
- ✅ ما يحتاج أي تعديلات
- ✅ يشتغل من أي مكان في العالم

---

## 🚨 ملاحظة مهمة:

**للاستخدام المؤقت (تجربة):**
- استخدم `0.0.0.0:8000` + افتح Firewall

**للاستخدام الدائم (للعامة):**
- استخدم **Ngrok** أو **PythonAnywhere**

---

## 📞 هل لسا ما اشتغل؟

جرّب:
1. أطفئ Antivirus مؤقتاً
2. أعد تشغيل الكمبيوتر
3. استخدم Ngrok (أضمن حل)

---

**الحل الأسرع: Ngrok! ⚡**
