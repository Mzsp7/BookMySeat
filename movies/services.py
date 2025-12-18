import stripe
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.db.models import Count
from .models import Seat, Booking, Movie, Theater, StripeWebhookEvent
from django.contrib.auth.models import User

# Initialize Stripe
try:
    stripe.api_key = settings.STRIPE_SECRET_KEY
except AttributeError:
    stripe = None

def clean_expired_seats(theater_id=None):
    """
    Releases all seat locks that have exceeded the lock duration.
    If theater_id is provided, focuses on that theater (though implementation is global).
    """
    lock_duration = getattr(settings, 'SEAT_LOCK_DURATION', 300)
    expired_time = timezone.now() - timedelta(seconds=lock_duration)
    
    query = Seat.objects.filter(status='locked', locked_at__lt=expired_time)
    
    # Efficient bulk update
    count = query.update(status='available', locked_by=None, locked_at=None)
    return count

def create_stripe_checkout_session(user, theater, seats, success_url, cancel_url):
    """
    Creates a Stripe Checkout Session for the locked seats.
    """
    if not stripe:
        raise Exception("Stripe is not configured.")

    # stripe setup is handled globally or default client is used

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': f'Movie Tickets: {theater.movie.name}',
                    'description': f'{len(seats)} seats at {theater.name}',
                },
                'unit_amount': 20000 * len(seats), # 200.00 INR (dummy price)
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            'theater_id': theater.id,
            'user_id': user.id,
            'seat_ids': ','.join([str(s.id) for s in seats]),
        },
        client_reference_id=str(user.id)
    )
    return checkout_session.url

def confirm_booking_from_session(session_data):
    """
    Process stable booking after successful payment.
    Handles atomic booking creation and async email confirmation.
    """
    metadata = session_data.get('metadata', {})
    theater_id = metadata.get('theater_id')
    user_id = metadata.get('user_id')
    seat_ids_str = metadata.get('seat_ids')
    payment_intent = session_data.get('payment_intent', 'manual_entry')
    
    if not (theater_id and user_id and seat_ids_str):
        return False

    seat_ids = seat_ids_str.split(',')
    
    try:
        # Atomic Transaction: Ensure all seats booked or none
        with transaction.atomic():
            user = User.objects.get(id=user_id)
            theater = Theater.objects.get(id=theater_id)
            seats = Seat.objects.filter(id__in=seat_ids)
            
            for seat in seats:
                # Idempotency/Safety: If booked by US, ignore. If booked by OTHER, skip/log.
                if seat.status == 'booked' and seat.locked_by != user:
                     continue
                
                # Mark as booked
                seat.status = 'booked'
                seat.locked_by = user 
                seat.save()
                
                # Idempotency: Check if booking already exists
                if Booking.objects.filter(seat=seat).exists():
                    continue

                # Create Booking Record
                Booking.objects.create(
                    user=user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater,
                    payment_id=payment_intent
                )
            
            # Application Logic: Schedule Email
            transaction.on_commit(lambda: _send_confirmation_email(user, theater, seat_ids, payment_intent))
            return True

    except Exception as e:
        print(f"Booking confirmation failed: {e}")
        return False

def _send_confirmation_email(user, theater, seat_ids, reference_id):
    """Async helper to send booking email."""
    bookings = Booking.objects.filter(
        user=user, 
        theater=theater, 
        seat__id__in=seat_ids,
        is_email_sent=False
    )
    
    if bookings.exists():
        seat_numbers = [b.seat.seat_number for b in bookings]
        subject = f"Your Confirmation for {theater.movie.name}"
        message = f"""
        Hello {user.username},

        Your booking is confirmed!

        Movie:   {theater.movie.name}
        Theater: {theater.name}
        Time:    {theater.time}
        Seats:   {', '.join(seat_numbers)}
        
        Ref ID:  {reference_id}
        
        Enjoy the movie!
        """
        
        try:
            print(f"DEBUG: Attempting to send email via {settings.EMAIL_HOST_USER} to {user.email}")
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            print(f"DEBUG: Email sent successfully to {user.email}")
            
            # Update is_email_sent
            Booking.objects.filter(payment_id=reference_id).update(is_email_sent=True)
        except Exception as e:
            print(f"CRITICAL ERROR: Email failed for User {user.email}: {e}")

def get_admin_metrics(time_filter='7'):
    """Calculates dashboard metrics safely."""
    now = timezone.now()
    if time_filter == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_filter == '30':
        start_date = now - timedelta(days=30)
    else: # Default 7
        start_date = now - timedelta(days=7)
    
    confirmed_bookings = Booking.objects.filter(
        booked_at__gte=start_date,
        seat__status='booked'
    )
    
    total_bookings = confirmed_bookings.count()
    PRICE_PER_SEAT = 200
    total_revenue = total_bookings * PRICE_PER_SEAT
    
    most_booked_movies = (
        confirmed_bookings.values('movie__name')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')[:5]
    )
    
    most_active_theaters = (
        confirmed_bookings.values('theater__name')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')[:5]
    )
    
    recent_bookings = (
        confirmed_bookings.select_related('user', 'movie', 'theater', 'seat')
        .order_by('-booked_at')[:10]
    )

    return {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'most_booked_movies': most_booked_movies,
        'most_active_theaters': most_active_theaters,
        'recent_bookings': recent_bookings,
        'start_date': start_date
    }
