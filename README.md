Installation

# Create a new virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

create requirements.txt
# Save it in C:\Users\abhil\Documents\PYTHON\Django\Django REST API Chat System\requirements.txt

pip install -r requirements.txt


# Test the API endpoints using Postman 

# Create a new Django project and app:
django-admin startproject chat_system
cd chat_system
python manage.py startapp chat_api


# Run migrations:
python manage.py makemigrations
python manage.py migrate


# Run the development server:
python manage.py runserver


# 1.Register a user:
POST http://localhost:8000/api/register/
{
    "username": "testuser",
    "password": "testpass123"
}


# 2.Login:
POST http://localhost:8000/api/login/
{
    "username": "testuser",
    "password": "testpass123"
}


# 3.Send a chat message:
POST http://localhost:8000/api/chat/
Authorization: <token-from-login>
{
    "message": "Hello, AI!"
}


# 4.Check token balance:
GET http://localhost:8000/api/balance/
Authorization: <token-from-login>


# Thank You 🙏
