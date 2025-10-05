web: cd gov_services && python manage.py migrate --noinput && python manage.py create_admin && gunicorn gov_services.wsgi:application --bind 0.0.0.0:$PORT --log-file -
