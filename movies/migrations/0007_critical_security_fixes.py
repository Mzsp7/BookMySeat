# Manual migration for critical fixes

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_movie_trailer_url'),
    ]

    operations = [
        # Fix #2: Add unique constraint on seat
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('theater', 'seat_number')},
        ),
        migrations.AddIndex(
            model_name='seat',
            index=models.Index(fields=['theater', 'status'], name='movies_seat_theater_status_idx'),
        ),
        
        # Fix #15: Change Booking.seat from OneToOne to ForeignKey
        migrations.AlterField(
            model_name='booking',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='movies.seat'),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('seat', 'theater')},
        ),
        
        # Fix #5: Add webhook idempotency tracking
        migrations.CreateModel(
            name='StripeWebhookEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('event_type', models.CharField(max_length=100)),
                ('processed_at', models.DateTimeField(auto_now_add=True)),
                ('payload', models.TextField(blank=True)),
            ],
        ),
    ]
