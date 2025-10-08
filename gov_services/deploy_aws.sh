#!/bin/bash

# ========================================
# سكريبت نشر Django على AWS Lightsail
# ========================================

echo "🚀 بدء عملية النشر على AWS Lightsail..."

# ألوان للطباعة
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# معلومات المشروع
PROJECT_NAME="gov_services"
PROJECT_DIR="/home/ubuntu/police-portal"
VENV_DIR="$PROJECT_DIR/venv"
APP_DIR="$PROJECT_DIR/gov_services"

# ========================================
# 1. تحديث النظام
# ========================================
echo -e "${YELLOW}📦 تحديث النظام...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

# ========================================
# 2. تثبيت المتطلبات الأساسية
# ========================================
echo -e "${YELLOW}📦 تثبيت المتطلبات...${NC}"
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    supervisor

# ========================================
# 3. إنشاء قاعدة البيانات PostgreSQL
# ========================================
echo -e "${YELLOW}🗄️ إعداد قاعدة البيانات...${NC}"

# توليد كلمة مرور عشوائية آمنة
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

# إنشاء قاعدة البيانات
sudo -u postgres psql <<EOF
CREATE DATABASE police_portal_db;
CREATE USER police_portal_user WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE police_portal_user SET client_encoding TO 'utf8';
ALTER ROLE police_portal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE police_portal_user SET timezone TO 'Asia/Dubai';
GRANT ALL PRIVILEGES ON DATABASE police_portal_db TO police_portal_user;
\q
EOF

echo -e "${GREEN}✅ قاعدة البيانات جاهزة${NC}"

# ========================================
# 4. استنساخ المشروع من GitHub
# ========================================
echo -e "${YELLOW}📥 استنساخ المشروع من GitHub...${NC}"

cd /home/ubuntu
if [ -d "$PROJECT_DIR" ]; then
    echo "المشروع موجود، سيتم تحديثه..."
    cd $PROJECT_DIR
    git pull origin main
else
    git clone https://github.com/hamad26650/police-ae.git police-portal
    cd $PROJECT_DIR
fi

# ========================================
# 5. إنشاء البيئة الافتراضية
# ========================================
echo -e "${YELLOW}🐍 إنشاء البيئة الافتراضية...${NC}"

python3.11 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# ========================================
# 6. تثبيت المتطلبات
# ========================================
echo -e "${YELLOW}📦 تثبيت متطلبات Python...${NC}"

cd $APP_DIR
pip install --upgrade pip
pip install -r requirements.txt

# ========================================
# 7. إنشاء ملف .env
# ========================================
echo -e "${YELLOW}⚙️ إنشاء ملف .env...${NC}"

# توليد SECRET_KEY عشوائي
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

cat > $APP_DIR/.env <<EOF
# Django Settings
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_DEBUG=False

# Database
DATABASE_URL=postgresql://police_portal_user:$DB_PASSWORD@localhost:5432/police_portal_db

# Email Configuration (سيتم إضافتها يدوياً)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Allowed Hosts (غيّره لدومينك)
ALLOWED_HOSTS=*.amazonaws.com,*.lightsail.aws.amazon.com

# CSRF Trusted Origins (غيّره لدومينك)
CSRF_TRUSTED_ORIGINS=https://*.amazonaws.com,https://*.lightsail.aws.amazon.com
EOF

echo -e "${GREEN}✅ ملف .env جاهز${NC}"

# ========================================
# 8. تطبيق Migrations
# ========================================
echo -e "${YELLOW}🗄️ تطبيق migrations...${NC}"

python manage.py migrate

# ========================================
# 9. جمع الملفات الثابتة
# ========================================
echo -e "${YELLOW}📁 جمع الملفات الثابتة...${NC}"

python manage.py collectstatic --noinput

# ========================================
# 10. إنشاء مستخدم admin
# ========================================
echo -e "${YELLOW}👤 إنشاء مستخدم admin...${NC}"
echo "ملاحظة: ستحتاج إنشاء المستخدم يدوياً بعد النشر"
echo "استخدم: python manage.py createsuperuser"

# ========================================
# 11. إعداد Gunicorn
# ========================================
echo -e "${YELLOW}⚙️ إعداد Gunicorn...${NC}"

# إنشاء ملف خدمة gunicorn
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=Gunicorn daemon for Police Portal
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn \\
    --workers 3 \\
    --bind unix:$APP_DIR/gunicorn.sock \\
    --timeout 120 \\
    gov_services.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# تفعيل وتشغيل gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo -e "${GREEN}✅ Gunicorn جاهز${NC}"

# ========================================
# 12. إعداد Nginx
# ========================================
echo -e "${YELLOW}⚙️ إعداد Nginx...${NC}"

# إنشاء ملف تكوين nginx
sudo tee /etc/nginx/sites-available/police_portal > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/police-portal/gov_services/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/police-portal/gov_services/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }
}
EOF

# تفعيل الموقع
sudo ln -sf /etc/nginx/sites-available/police_portal /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# اختبار تكوين nginx
sudo nginx -t

# إعادة تشغيل nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

echo -e "${GREEN}✅ Nginx جاهز${NC}"

# ========================================
# 13. إعداد Firewall
# ========================================
echo -e "${YELLOW}🔒 إعداد Firewall...${NC}"

sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

echo -e "${GREEN}✅ Firewall جاهز${NC}"

# ========================================
# 14. معلومات النشر
# ========================================
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 تم النشر بنجاح!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${YELLOW}📝 معلومات مهمة:${NC}"
echo -e "قاعدة البيانات: police_portal_db"
echo -e "المستخدم: police_portal_user"
echo -e "كلمة المرور: $DB_PASSWORD"
echo -e "\n${YELLOW}⚠️ احفظ كلمة المرور في مكان آمن!${NC}\n"

echo -e "${YELLOW}📋 الخطوات التالية:${NC}"
echo -e "1. عدّل ملف .env وأضف معلومات Gmail:"
echo -e "   ${GREEN}nano $APP_DIR/.env${NC}"
echo -e ""
echo -e "2. أنشئ مستخدم admin:"
echo -e "   ${GREEN}cd $APP_DIR${NC}"
echo -e "   ${GREEN}source $VENV_DIR/bin/activate${NC}"
echo -e "   ${GREEN}python manage.py createsuperuser${NC}"
echo -e ""
echo -e "3. احصل على IP العام من AWS Console"
echo -e ""
echo -e "4. افتح المتصفح واذهب إلى:"
echo -e "   ${GREEN}http://YOUR_IP_ADDRESS${NC}"
echo -e ""
echo -e "${GREEN}🚀 الموقع جاهز للاستخدام!${NC}\n"

# حفظ معلومات قاعدة البيانات
echo "DB_PASSWORD=$DB_PASSWORD" > /home/ubuntu/db_credentials.txt
chmod 600 /home/ubuntu/db_credentials.txt

echo -e "${YELLOW}💡 معلومات قاعدة البيانات محفوظة في:${NC}"
echo -e "   ${GREEN}/home/ubuntu/db_credentials.txt${NC}\n"

