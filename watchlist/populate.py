import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMDB.settings")

import django
django.setup()

from faker import Faker
from django.contrib.auth.models import User
from watchlist.models import WatchList, StreamPlatform, Review

fake = Faker()

# Create StreamPlatform instances
for _ in range(5):
    platform = StreamPlatform.objects.create(
        name=fake.company(),
        about=fake.text(max_nb_chars=150),
        website=fake.url()
    )

# Create WatchList instances
for _ in range(20):
    watchlist = WatchList.objects.create(
        title=fake.catch_phrase(),
        storyline=fake.text(max_nb_chars=200),
        platform=StreamPlatform.objects.order_by("?").first(),
        active=fake.boolean(chance_of_getting_true=70)
    )

# Create Review instances
for watchlist in WatchList.objects.all():
    for _ in range(fake.random_int(min=0, max=5)):  # Create 0-4 reviews per WatchList
        user = User.objects.order_by("?").first()  # Randomly select a user
        Review.objects.create(
            user=user,
            rating=fake.random_int(min=1, max=5),
            description=fake.paragraph(nb_sentences=3),
            watchlist=watchlist,
            active=fake.boolean(chance_of_getting_true=90)
        )

print("Dummy data has been added successfully.")
