# Generated manually for trailer_url field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_booking_is_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_url',
            field=models.URLField(blank=True, help_text='YouTube trailer URL', max_length=500, null=True),
        ),
    ]
