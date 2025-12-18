
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
django.setup()

from movies.models import Movie, Theater
from django.utils import timezone
from datetime import timedelta

def populate():
    movies_data = [
        {
            'name': 'Inception',
            'trailer_url': 'https://www.youtube.com/watch?v=YoHD9XEInc0',
            'genre': 'Sci-Fi / Action',
            'rating': 8.8,
            'image': 'movies/inception.png',
            'language': 'English'
        },
        {
            'name': 'The Dark Knight',
            'trailer_url': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
            'genre': 'Action / Drama',
            'rating': 9.0,
            'image': 'movies/dark_knight.png',
            'language': 'English'
        },
        {
            'name': 'Interstellar',
            'trailer_url': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
            'genre': 'Sci-Fi / Drama',
            'rating': 8.7,
            'image': 'movies/interstellar.png',
            'language': 'English'
        },
        {
            'name': 'Avatar: The Way of Water',
            'trailer_url': 'https://www.youtube.com/watch?v=d9MyW72ELq0',
            'genre': 'Action / Sci-Fi',
            'rating': 7.6,
            'image': 'movies/avatar.png',
            'language': 'English'
        }
    ]

    for data in movies_data:
        movie, created = Movie.objects.update_or_create(
            name=data['name'],
            defaults={
                'trailer_url': data['trailer_url'],
                'genre': data['genre'],
                'rating': data['rating'],
                'image': data['image'],
                'language': data['language']
            }
        )
        print(f"{'Created' if created else 'Updated'}: {movie.name}")

        # Add a placeholder theater if none exists
        if not movie.theaters.exists():
            Theater.objects.create(
                name=f"Cinema Hall 1 - {movie.name}",
                movie=movie,
                time=timezone.now() + timedelta(days=1, hours=18)
            )
            print(f"Added theater for {movie.name}")

if __name__ == '__main__':
    populate()
