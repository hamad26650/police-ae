# 🚀 البداية السريعة - AWS Lightsail

## ⚡ 3 خطوات فقط!

---

### 1️⃣ سجّل في AWS:
👉 https://lightsail.aws.amazon.com/
- اختر: Middle East (Bahrain) 🇧🇭
- خطة: $5/شهر

---

### 2️⃣ افتح SSH Terminal في Lightsail

---

### 3️⃣ شغّل هذي الأوامر:

```bash
cd /home/ubuntu
git clone https://github.com/hamad26650/police-ae.git police-portal
cd police-portal/gov_services
chmod +x deploy_aws.sh
sudo ./deploy_aws.sh
```

⏰ انتظر 5-10 دقائق...

---

## ✅ تم!

**بعدها:**

1. عدّل Gmail في `.env`:
```bash
nano /home/ubuntu/police-portal/gov_services/.env
```

2. أنشئ admin:
```bash
cd /home/ubuntu/police-portal/gov_services
source /home/ubuntu/police-portal/venv/bin/activate
python manage.py createsuperuser
```

3. افتح موقعك:
```
http://YOUR_IP_ADDRESS
```

---

📖 **للتفاصيل الكاملة:** اقرأ [DEPLOY_AWS_LIGHTSAIL.md](DEPLOY_AWS_LIGHTSAIL.md)

