from .models import User

def get_users_with_upcoming_taxes():
    from datetime import timedelta, date
    today = date.today()
    return User.objects.filter(tax_due_date__in=[today + timedelta(days=30), today + timedelta(days=7)])
