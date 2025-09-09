from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="winner")
    title = models.CharField(max_length=32)
    image = models.URLField(max_length=128)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    start_price = models.FloatField()
    current_bid = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField()

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete= models.CASCADE, related_name="bids")
    bid = models.FloatField()

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=128)

