from celery import shared_task
from datetime import datetime,timedelta
# from django.core.mail import send_mail
from celery.schedules import crontab
from booking.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string

@shared_task()
def success_message(email,messages):
  subject ="Booking Successful"
  message = messages

  recipients = [email]
  send_mail(subject,message,None,recipients)
  return subject

@shared_task()
def send_rating_reminder():
  today = datetime.now().date()
  yesterday = today - timedelta(days=1)

  bookings_for_yesterday = Booking.objects.filter(checkout_date=yesterday)

  for booking in bookings_for_yesterday:
    subject = f"Rate Your Stay - Booking ID {booking.id}"
    template_name = 'rate_feedback.html'
    context = {
        'user': booking.user.username,
        'rate_url': f"http://127.0.0.1:8000/add/ratting/{booking.hotel.id}/",
    }
    message = render_to_string(template_name, context)

    send_mail(subject, message, None, [booking.user.email], html_message=message)
    print(f"Rating reminder sent for booking ID {booking.id}")
    
@shared_task()
def cancel_booking_message(email,messages):
  print(3345435)
  subject ="cancel Booking"
  message = messages
  recipients = [email]
  send_mail(subject,message,None,recipients)
  return subject