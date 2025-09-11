from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
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
                          start_price=start_price,
                          current_bid = None,
                          is_active=True
                          )
        
        listing.save()
        return HttpResponseRedirect(reverse("create-listing"))
    
    return render(request, "auctions/create-listing.html")

def place_bid(user, listing, bid):
    
    if listing.current_bid is None:
        if bid < listing.start_price:
            return "Your bid must be equal or higher than the starting price."
    else:
        if bid <= listing.current_bid:
            return "Your bid must be higher than the current highest bid."
        
    new_bid = Bid(listing=listing, bidder=user, bid=bid) 
    new_bid.save()
    listing.current_bid = bid
    listing.save()
    return "Your Bid was successfully placed."
    

@login_required
def listing_page_view(request, number):
    user = request.user
    listing = Listing.objects.get(pk = number)
    if listing.watchers.filter(id=user.id).exists():
        is_watched = True
    else:
        is_watched = False
    comments = listing.comments.all()
    
    if request.method == "POST":
        match request.POST["form-type"]:
            case "close_listing":
                listing.is_active = False
                highest_bid = listing.bids.order_by("-bid").first()
                if highest_bid:
                    listing.winner = highest_bid.bidder
                listing.save()
                return HttpResponseRedirect(reverse("listing-page", kwargs={"number": number}))
            case "place_bid":
                try:
                    bid = float(request.POST["bid"].strip())
                except ValueError:
                    return render(request,"auctions/listing-page.html", {
                        "listing": listing,
                        "number": number,
                        "is_watched": is_watched,
                        "comments": comments,
                        "message": "Error! Please enter a valid number."
                    })
                message = place_bid(user, listing, bid)
                return render(request,"auctions/listing-page.html", {
                        "listing": listing,
                        "number": number,
                        "is_watched": is_watched,
                        "comments": comments,
                        "message": message
                    })
            case "add_watchlist":
                listing.watchers.add(user)
                is_watched = True
            case "remove_watchlist":
                listing.watchers.remove(user)
                is_watched = False
            case "comment":
                comment = request.POST["comment"]
                if comment:
                    user = request.user
                    new_comment = Comment(
                        listing = listing,
                        author = user,
                        comment = comment
                    )
                    new_comment.save()
                comments = listing.comments.all()
    
    return render(request, "auctions/listing-page.html", {
        "listing": listing,
        "number": number,
        "is_watched": is_watched,
        "comments": comments
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

def categories_view(request):
    listings = Listing.objects.all()
    categories = set()
    for listing in listings:
        categories.add(listing.category)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def specific_category_view(request, category_name):
    listings = Listing.objects.filter(category = category_name, is_active = True)
    return render(request, "auctions/specific-category.html", {
        "category_name": category_name,
        "listings": listings
    })
