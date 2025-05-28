echo "Running Django setup script..."


rm -f "db.sqlite3"

python3 manage.py makemigrations
python3 manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_user(username='youcef.ely', email='youcef.lyousfi@example.com', password='S3cret!', role='supervisor')" | python manage.py shell