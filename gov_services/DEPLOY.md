# دليل نشر الموقع على سيرفر حقيقي

## المتطلبات الأساسية

1. **Python 3.10+**
2. **PostgreSQL** (موصى به للإنتاج)
3. **Nginx** (لخدمة الملفات الثابتة)
4. **Gunicorn** (خادم WSGI)
5. **Domain name** (اسم نطاق)

---

## الخطوة 1: إعداد السيرفر

### على Ubuntu/Debian:

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و PostgreSQL
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y

# إنشاء مستخدم جديد للمشروع
sudo adduser govservices
sudo su - govservices
```

---

## الخطوة 2: رفع الملفات

```bash
# على السيرفر
cd /home/govservices
git clone your-repo-url gov_services
# أو استخدم SCP/SFTP لرفع الملفات
```

---

## الخطوة 3: إعداد البيئة الافتراضية

```bash
cd /home/govservices/gov_services
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## الخطوة 4: إعداد قاعدة البيانات

```bash
# إنشاء قاعدة بيانات PostgreSQL
sudo -u postgres psql
CREATE DATABASE gov_services_db;
CREATE USER govservices_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE gov_services_db TO govservices_user;
\q
```

---

## الخطوة 5: إعداد متغيرات البيئة

```bash
cd /home/govservices/gov_services
cp .env.example .env
nano .env
```

عدّل الملف `.env`:

```env
DJANGO_SECRET_KEY=your-very-secure-secret-key-here
DJANGO_DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://govservices_user:your-secure-password@localhost:5432/gov_services_db

EMAIL_HOST_USER=Project.test85@outlook.com
EMAIL_HOST_PASSWORD=your-app-password-here
```

---

## الخطوة 6: إعداد Django

```bash
source venv/bin/activate
cd gov_services

# تشغيل migrations
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إنشاء مستخدم admin
python manage.py createsuperuser
```

---

## الخطوة 7: إعداد Gunicorn

أنشئ ملف `/home/govservices/gov_services/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
timeout = 120
keepalive = 5
```

أنشئ ملف systemd service `/etc/systemd/system/govservices.service`:

```ini
[Unit]
Description=Gov Services Gunicorn daemon
After=network.target

[Service]
User=govservices
Group=www-data
WorkingDirectory=/home/govservices/gov_services/gov_services
ExecStart=/home/govservices/gov_services/venv/bin/gunicorn \
    --config /home/govservices/gov_services/gunicorn_config.py \
    gov_services.wsgi:application

Restart=always

[Install]
WantedBy=multi-user.target
```

تفعيل الخدمة:

```bash
sudo systemctl daemon-reload
sudo systemctl enable govservices
sudo systemctl start govservices
sudo systemctl status govservices
```

---

## الخطوة 8: إعداد Nginx

أنشئ ملف `/etc/nginx/sites-available/govservices`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # إعادة توجيه HTTP إلى HTTPS (بعد تثبيت SSL)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/govservices/gov_services/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/govservices/gov_services/media/;
    }
}
```

تفعيل الموقع:

```bash
sudo ln -s /etc/nginx/sites-available/govservices /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## الخطوة 9: تثبيت SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## الخطوة 10: إعدادات الأمان

### تحديث settings.py:

```python
# في الإنتاج
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## الخطوة 11: إعدادات البريد الإلكتروني

تأكد من:
1. إعدادات Outlook صحيحة في `.env`
2. استخدام App Password إذا كان التحقق الثنائي مفعّل
3. تحديث إيميلات البنوك في `services/utils/email_service.py`

---

## الصيانة

### عرض logs:

```bash
# Gunicorn logs
sudo journalctl -u govservices -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### إعادة تشغيل الخدمات:

```bash
sudo systemctl restart govservices
sudo systemctl restart nginx
```

### تحديث الموقع:

```bash
cd /home/govservices/gov_services
source venv/bin/activate
git pull  # أو رفع الملفات الجديدة
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart govservices
```

---

## استكشاف الأخطاء

1. **خطأ 502 Bad Gateway:**
   - تحقق من أن Gunicorn يعمل: `sudo systemctl status govservices`
   - تحقق من logs: `sudo journalctl -u govservices -n 50`

2. **الملفات الثابتة لا تظهر:**
   - تأكد من تشغيل `collectstatic`
   - تحقق من صلاحيات المجلد: `sudo chown -R www-data:www-data staticfiles/`

3. **خطأ في قاعدة البيانات:**
   - تحقق من إعدادات DATABASE_URL في `.env`
   - تأكد من أن PostgreSQL يعمل: `sudo systemctl status postgresql`

---

## ملاحظات مهمة

- ✅ استخدم كلمات مرور قوية
- ✅ احتفظ بنسخة احتياطية من قاعدة البيانات
- ✅ راقب استخدام الموارد (CPU, RAM, Disk)
- ✅ قم بتحديث النظام بانتظام
- ✅ استخدم firewall (UFW)

---

## الدعم

للمساعدة، راجع:
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Gunicorn Docs: https://docs.gunicorn.org/
- Nginx Docs: https://nginx.org/en/docs/


