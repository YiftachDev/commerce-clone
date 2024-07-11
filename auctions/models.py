from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.category}"


class Listings(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=100)
    price = models.IntegerField()
    sold = models.BooleanField(default=False)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="selected_category")
    user = models.ForeignKey(User, on_delete=models.CASCADE) #the user that posted the item

    def __str__(self):
        return f"{self.title} posted by {self.user}"


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_comment")

    def __str__(self):
        return f"comment by-{self.user}: {self.comment}"


class Bid(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bil")
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bil")

    def __str__(self):
        return f"bid on item: {self.listing} by {self.user} with price: {self.amount}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")
    watching = models.BooleanField(default=False)

