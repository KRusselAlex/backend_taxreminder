![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)


# 📧 backend_taxReminder Backend

Atax Reminder is a backend service built to automate and schedule **payment reminders** via **Email** and **SMS**. It offers a robust RESTful API using **Django REST Framework** for client and reminder management. The system handles background jobs using **Celery** and **Celery Beat**, powered by **Redis**. PostgreSQL serves as the primary database. **Twilio** is used for SMS delivery and **Gmail SMTP** for emails.

---

## 🚀 Tech Stack

- **Django** – High-level Python web framework
- **Django REST Framework (DRF)** – Powerful toolkit for building Web APIs
- **Celery** – Asynchronous task processing
- **Celery Beat** – Scheduler for periodic jobs
- **Redis** – Message broker & result backend
- **PostgreSQL** – Relational database
- **Twilio** – SMS reminder service
- **Gmail SMTP** – Email reminders
- **Docker** (optional) – For containerized development

---

## 📁 Project Structure

```
backend_taxreminder/
│
├── backend_taxreminder/       # Django project config
│   ├── settings.py
│   ├── celery.py
│   └── __init__.py
│
├── notifications/           # Core app
│   ├── models.py
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # API routes
│   ├── tasks.py         # Celery tasks for email/SMS
│   └── admin.py
├── clients/           # Core app
│   ├── models.py
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # API routes
│   ├── tasks.py         # Celery tasks for email/SMS
│   └── admin.py
├── users/           # Core app
│   ├── models.py
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # API routes
│   ├── tasks.py         # Celery tasks for email/SMS
│   └── admin.py
├── reports/           # Core app
│   ├── models.py
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # API routes
│   ├── tasks.py         # Celery tasks for email/SMS
│   └── admin.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧰 Prerequisites

Make sure you have the following installed:

- Python 3.10+
- PostgreSQL
- Redis
- pip or virtualenv / pipenv
- (Optional) Docker & Docker Compose

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/atax-reminder-backend.git
cd atax-reminder-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure `djangorestframework`, `celery`, `redis`, `twilio`, and `python-dotenv` are listed in your `requirements.txt`.

### 4. Set environment variables

Create a `.env` file:

```env
# Email (Gmail)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Twilio
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# General
ENVIRONMENT=dev

# PostgreSQL
DATABASE_URL=

# Redis (for Celery)
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

---

## 🧪 API Usage

Django REST Framework is used to expose the API for interacting with reminders and clients.

### Example Endpoints

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| GET    | `/api/notifications/` | List all reminders         |
| POST   | `/api/notifications/` | Create new reminder        |
| GET    | `/api/clients/`       | List all clients           |
| POST   | `/api/clients/`       | Add a new client           |
| POST   | `/api/reports/`       | send a new reports via mail|



> All endpoints are powered by **DRF ViewSets** and **Serializers**.

---

## ⚙️ Running Celery & Celery Beat

### 1. Start Redis (locally or via Docker)

```bash
docker run -p 6379:6379 redis
```

### 2. Start Celery worker

```bash
celery -A atax_reminder worker --loglevel=info
```

### 3. Start Celery Beat

```bash
celery -A atax_reminder beat --loglevel=info
```

---

## ✉️ Sending Email Reminders

```python
@shared_task
def send_reminder_email(to_email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
```

---

## 📲 Sending SMS Reminders with Twilio

```python
@shared_task
def send_reminder_sms(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number
    )
```

---

## 🧪 Run Tests

```bash
python manage.py test
```

---

## 🐳 Docker Support (Coming Soon)

We'll be adding a `docker-compose.yml` file to run PostgreSQL, Redis, Django, Celery, and Celery Beat together.

---

## 🤝 Contributing

Feel free to fork, raise issues, or open pull requests!

---

## 📫 Contact

**Developer:** Kouawou Alex  
**Email:** kouawoualex1234@gmail.com  

