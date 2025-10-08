#!/bin/bash
# سكريبت لجمع الملفات الثابتة

echo "🔄 جاري جمع الملفات الثابتة..."

# جمع جميع الملفات الثابتة
python manage.py collectstatic --noinput --clear

echo "✅ تم جمع الملفات الثابتة بنجاح!"
echo "📊 عدد الملفات:"
ls -la staticfiles/ | wc -l

echo ""
echo "✅ الصور والشعارات جاهزة!"

