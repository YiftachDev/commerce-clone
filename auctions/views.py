from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listing":Listings.objects.filter(sold=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add_listing(request):
    if request.method == "POST":
        listing_title = request.POST["title"]
        listing_description = request.POST["description"]
        listing_image = request.POST["image"]
        listing_stating_bid = request.POST["bid"]
        user = request.user
        category = Category.objects.get(id=request.POST["categories"])
        Listings.objects.create(title=listing_title, description=listing_description, image=listing_image, price=listing_stating_bid, user=user, category=category)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/add_listing.html", {
        "categories": Category.objects.all()
    })


@login_required
def listing(request, listing_t):
    listing = Listings.objects.get(title=listing_t)
    if request.method == "POST":
        comment = request.POST["comment"]
        Comment.objects.create(comment=comment, user=request.user, listing=listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_t,)))
    return render(request, "auctions/listing.html", {
        "title": listing.title,
        "image": listing.image,
        "description": listing.description,
        "user": listing.user,
        "category": listing.category,
        "price": listing.price,
        "id": listing.id,
        "commants": Comment.objects.filter(listing=listing.id),
        "watching": WatchList.objects.filter(listing=listing.id)
    })


@login_required
def bidding(request, listing_id):
    if request.method == "POST":
        bid = request.POST["bid"]
        listing = Listings.objects.get(id=listing_id)
        listing.price = int(bid)
        listing.save()
        Bid.objects.create(user=listing.user, amount=listing.price, listing=listing)
    return render(request, "auctions/listing.html", {
        "title": listing.title,
        "image": listing.image,
        "description": listing.description,
        "user": listing.user,
        "category": listing.category,
        "price": listing.price,
        "id": listing.id,
        "commants": Comment.objects.filter(listing=listing.id),
        "watching": WatchList.objects.filter(listing=listing.id)
    })