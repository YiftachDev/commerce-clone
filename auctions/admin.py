from django.contrib import admin
from .models import Bid, Category, Listings, User, WatchList, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Category)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(Comment)