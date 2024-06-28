from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class WatchList(models.Model):
    title = models.CharField(max_length=50, verbose_name="Movie title")
    storyline = models.CharField(max_length=200, verbose_name="Storyline")
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE ,related_name="watchlist")
    average_rating = models.FloatField(default=0, verbose_name="Average rating")
    number_of_rating = models.IntegerField(default=0, verbose_name="Number of rating")
    active = models.BooleanField(default=True, verbose_name="Active")
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self): 
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Rating")
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + "-" + str(self.watchlist.title)