"""
Script to add cinema-style seats to all theaters.
Creates a realistic seat layout with rows A-J and seats 1-12.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
django.setup()

from movies.models import Theater, Seat

def add_seats_to_theater(theater, rows=10, seats_per_row=12):
    """Add seats in a grid layout (A1, A2, ... J12)"""
    row_letters = 'ABCDEFGHIJ'[:rows]
    
    existing_seats = set(Seat.objects.filter(theater=theater).values_list('seat_number', flat=True))
    added_count = 0
    
    for row_letter in row_letters:
        for seat_num in range(1, seats_per_row + 1):
            seat_number = f"{row_letter}{seat_num}"
            
            if seat_number not in existing_seats:
                Seat.objects.create(
                    theater=theater,
                    seat_number=seat_number,
                    status='available'
                )
                added_count += 1
    
    return added_count

def main():
    theaters = Theater.objects.all()
    
    if not theaters.exists():
        print("❌ No theaters found. Please add movies and theaters first.")
        return
    
    print(f"🎬 Found {theaters.count()} theater(s)\n")
    
    total_added = 0
    for theater in theaters:
        existing = Seat.objects.filter(theater=theater).count()
        added = add_seats_to_theater(theater, rows=10, seats_per_row=12)
        total_added += added
        
        print(f"✅ {theater.name} ({theater.movie.name})")
        print(f"   Before: {existing} seats | Added: {added} seats | Total: {existing + added} seats\n")
    
    print(f"🎉 Successfully added {total_added} seats across all theaters!")
    print(f"📊 Total seats in system: {Seat.objects.count()}")

if __name__ == '__main__':
    main()
