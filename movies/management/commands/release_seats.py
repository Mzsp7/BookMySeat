from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from movies.models import Seat

from django.conf import settings

class Command(BaseCommand):
    help = 'Releases expired seat locks'

    def handle(self, *args, **options):
        lock_duration = getattr(settings, 'SEAT_LOCK_DURATION', 300)
        expiry_time = timezone.now() - timedelta(seconds=lock_duration)
        
        # Release expired locked seats
        updated_count = Seat.objects.filter(
            status='locked', 
            locked_at__lt=expiry_time
        ).update(status='available', locked_by=None, locked_at=None)
        
        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Released {updated_count} expired seats'))
        else:
            self.stdout.write(self.style.SUCCESS('No expired seats found'))
