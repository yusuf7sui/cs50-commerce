from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    if request.method == "POST":
        user = request.user
        listing_id = request.POST["listing-id"]
        listing = Listing.objects.get(pk=listing_id)
        listing.watchers.add(user)
        return HttpResponseRedirect(reverse("index"))
    
    active_listings = Listing.objects.filter(is_active = True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
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
    return HttpResponseRedirect(reverse("index"))


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
def create_listing(request):
    if request.method == "POST":
        owner = request.user # research how to get the username
        title = request.POST["title"].strip()
        image = request.POST["image"].strip()
        description = request.POST["description"].strip()
        category = request.POST["category"].strip()

        try:
            start_price = float(request.POST["start-price"].strip())
        except ValueError:
            return render(request,"auctions/create-listing.html", {
                "message": "Error! Please enter a valid number for the start price."
            })
        
        inputs = [title, image, description, category]
        if any(x == "" for x in inputs):
            return render(request,"auctions/create-listing.html", {
                "message": "Error! Please fill in all required fields."
            })

        listing = Listing(owner=owner, 
                          title = title,
                          image=image,
                          description=description, 
                          category=category, 
                          bid=start_price,
                          is_active=True
                          )
        
        listing.save()
        return HttpResponseRedirect(reverse("create-listing"))
    
    return render(request, "auctions/create-listing.html")

@login_required
def listing_page_view(request, number):
    if request.method == "POST":
        pass
    listing = Listing.objects.get(pk = number)
    return render(request, "auctions/listing-page.html", {
        "listing": listing,
        "number": number
    })

@login_required
def watchlist_view(request):
    user = request.user
    if request.method == "POST":
        listing_id = request.POST["listing-id"]
        listing = Listing.objects.get(pk=listing_id)
        listing.watchers.remove(user)
        return HttpResponseRedirect(reverse("watchlist"))

    watchlist = Listing.objects.filter(watchers = user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })