from django.db import models
from django.contrib.auth.models import User 


class Movie(models.Model):
    name= models.CharField(max_length=255)
    image= models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    cast= models.TextField()
    description= models.TextField(blank=True,null=True) # optional
    genre = models.CharField(max_length=100, default='Action')
    language = models.CharField(max_length=100, default='Hindi')
    trailer_url = models.URLField(max_length=500, blank=True, null=True, help_text="YouTube trailer URL")

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')
    time= models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('locked', 'Locked'),
        ('booked', 'Booked'),
    )
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    locked_at = models.DateTimeField(null=True, blank=True)
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = [['theater', 'seat_number']]
        indexes = [
            models.Index(fields=['theater', 'status']),
        ]

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name} - {self.status}'

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.ForeignKey(Seat,on_delete=models.CASCADE, related_name='bookings')
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE)
    booked_at=models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    is_email_sent = models.BooleanField(default=False)
    
    class Meta:
        unique_together = [['seat', 'theater']]
    
    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'

class StripeWebhookEvent(models.Model):
    """Track processed Stripe webhook events for idempotency"""
    event_id = models.CharField(max_length=255, unique=True, db_index=True)
    event_type = models.CharField(max_length=100)
    processed_at = models.DateTimeField(auto_now_add=True)
    payload = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.event_type} - {self.event_id}'