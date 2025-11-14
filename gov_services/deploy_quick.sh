#!/bin/bash
# سكريبت نشر سريع للموقع

echo "=========================================="
echo "   Gov Services - Quick Deploy Script"
echo "=========================================="
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    exit 1
fi

# التحقق من وجود virtual environment
if [ ! -d "venv" ]; then
    echo "📦 إنشاء virtual environment..."
    python3 -m venv venv
fi

# تفعيل virtual environment
echo "🔧 تفعيل virtual environment..."
source venv/bin/activate

# تثبيت المتطلبات
echo "📥 تثبيت المتطلبات..."
pip install --upgrade pip
pip install -r requirements.txt

# تشغيل migrations
echo "🗄️  تشغيل migrations..."
python manage.py migrate

# جمع الملفات الثابتة
echo "📁 جمع الملفات الثابتة..."
python manage.py collectstatic --noinput

echo ""
echo "✅ تم الإعداد بنجاح!"
echo ""
echo "الخطوات التالية:"
echo "1. قم بإعداد ملف .env مع المتغيرات المطلوبة"
echo "2. أنشئ مستخدم admin: python manage.py createsuperuser"
echo "3. شغل الموقع: gunicorn gov_services.wsgi:application --config gunicorn_config.py"
echo ""

