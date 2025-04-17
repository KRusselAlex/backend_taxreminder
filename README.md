
# 📧 Atax Reminder Backend

Atax Reminder is a backend service designed to automate the sending of payment reminders to clients via **Email** and **SMS**. It is built using **Django** and leverages **Celery** and **Redis** for asynchronous task processing and periodic task scheduling using **Celery Beat**. **Twilio** is used to send SMS reminders, and **Gmail SMTP** is used for sending emails. PostgreSQL is the main database.

---

## 🚀 Tech Stack

- **Django** – Backend web framework
- **Celery** – Task queue for background jobs
- **Celery Beat** – Scheduler for periodic tasks
- **Redis** – Message broker and result backend
- **PostgreSQL** – Relational database
- **Twilio** – SMS reminder service
- **Gmail SMTP** – For sending email reminders
- **Docker** (optional) – For easier deployment

---

## 📁 Project Structure

```
atax_reminder/
│
├── atax_reminder/       # Django project root
│   ├── settings.py
│   ├── celery.py
│   └── __init__.py
│
├── reminders/           # App with task logic
│   ├── models.py
│   ├── tasks.py         # Email & SMS tasks
│   ├── views.py
│   └── utils.py         # (Optional) SMS/Email utilities
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧰 Prerequisites

Ensure you have the following installed:

- Python 3.10+
- PostgreSQL
- Redis
- pip / virtualenv or pipenv
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

### 4. Set environment variables

Create a `.env` file in your root directory and add the following:

```env
# Email configuration (Gmail SMTP)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Environment setting
ENVIRONMENT=dev

# PostgreSQL Database
DATABASE_URL=

# Redis (Celery Broker & Backend)
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```

> **Warning:** For production, never expose your credentials in public repos.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

---

## ⚙️ Running Celery & Celery Beat

Make sure Redis is running (either locally or remotely).

### 1. Start Celery Worker

```bash
celery -A atax_reminder worker --loglevel=info
```

### 2. Start Celery Beat (for periodic/scheduled tasks)

```bash
celery -A atax_reminder beat --loglevel=info
```

---

## ✉️ Sending Email Reminders

You can define a Celery task in `notifications/tasks.py` like:

```python
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_reminder_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )
```

---

## 📲 Sending SMS Reminders

Example SMS task using Twilio:

```python
from celery import shared_task
from twilio.rest import Client
from django.conf import settings

@shared_task
def send_reminder_sms(to_number, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number
    )
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🐳 Docker Support (Coming Soon)

Docker and docker-compose support will be added to simplify running the full stack including Django, Redis, and PostgreSQL.

---

## 🤝 Contributing

Feel free to fork this repo, submit PRs, or open issues for improvements and features.

---

## 📫 Contact

**Developer:** Kouawou Alex  
**Email:** kouawoualex1234@gmail.com  

---

## 📄 License

This project is licensed under the MIT License.
