# Newborn Care Hub — Backend

**Ada Developers Academy — Cohort 24 Capstone Project**  
Built by Helen Larson

Backend API for **Newborn Care Hub**, a full-stack platform that connects families with newborn and postpartum care professionals.

🔗 **Live API:**  
https://newborn-care-hub-backend.onrender.com

## Tech Stack
- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL (Supabase)
- JWT Authentication
- Cloudinary (profile image storage)

---

## Main Features 
- JWT-based user authentication
- User roles: family & provider
- Provider profiles with image upload
- Reviews
- Messaging between users
- Django Admin panel

---

## Dependencies
This project relies on the following main dependencies:
- **Django**
- **djangorestframework**
- **djangorestframework-simplejwt**
- **django-cors-headers**
- **python-dotenv**
- **psycopg2-binary**
- **Pillow**
- **cloudinary**
- **django-cloudinary-storage**
- **gunicorn**

Additional dependencies are listed in the `requirements.txt` file.

---

## Setup Instructions

To run this project locally, follow the steps below:

1. Clone the repository:
    git clone <backend-repository-url>

2. Navigate to the project directory:
    cd backend

3. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate

4. Install dependencies:
    pip install -r requirements.txt

5. Create a .env file in the root directory and add the required environment variables:
    DJANGO_SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=your-database-connection-string
    CLOUDINARY_CLOUD_NAME=your-cloud-name
    CLOUDINARY_API_KEY=your-api-key
    CLOUDINARY_API_SECRET=your-api-secret

6. Run database migrations:
    python manage.py migrate

7. Create a superuser (optional, for admin access):
    python manage.py createsuperuser

8. Start the development server:
    python manage.py runserver

9. Open the API in your browser:
    http://localhost:8000

