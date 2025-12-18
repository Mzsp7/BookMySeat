"""
Manually send confirmation email for a specific booking
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
django.setup()

from movies.models import Booking
from django.core.mail import send_mail
from django.conf import settings

# Get the latest booking for mzsp_
booking = Booking.objects.filter(user__username='mzsp_').order_by('-id').first()

if booking:
    print(f"📧 Sending confirmation email for Booking #{booking.id}")
    print(f"   User: {booking.user.username}")
    print(f"   Email: {booking.user.email}")
    print(f"   Movie: {booking.theater.movie.name}")
    print(f"   Seat: {booking.seat.seat_number}\n")
    
    subject = f"Your Confirmation for {booking.theater.movie.name}"
    message = f"""
Hello {booking.user.username},

Your booking is confirmed!

Movie:   {booking.theater.movie.name}
Theater: {booking.theater.name}
Time:    {booking.theater.time}
Seat:    {booking.seat.seat_number}

Ref ID:  {booking.payment_id or 'N/A'}

Enjoy the movie!

---
BookMySeat Team
    """
    
    print("=" * 60)
    print("EMAIL CONTENT:")
    print("=" * 60)
    print(f"To: {booking.user.email}")
    print(f"From: {settings.EMAIL_HOST_USER}")
    print(f"Subject: {subject}")
    print(message)
    print("=" * 60)
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.user.email],
            fail_silently=False
        )
        print("\n✅ Email sent successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
else:
    print("❌ No bookings found for user 'mzsp_'")
