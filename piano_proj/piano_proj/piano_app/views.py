from django.shortcuts import render
from django.http import (
    HttpResponse, 
    HttpResponseRedirect, 
    JsonResponse, 
    HttpResponseForbidden,
    HttpResponseNotAllowed
)
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django import forms
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from django.forms import ModelForm
from .models import User, Piano, Comment, Vote


# ----------------------------------------------------------------
# Forms
# ----------------------------------------------------------------

# ModelForm class to create a piano
class CreatePianoForm(ModelForm):
    class Meta:
        model = Piano
        fields = ['brand', 'price', 'size', 'imageUrl']
   
   # Add class to all visible model form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control mb-3"


# Form from 'Form' class
class CreatePianoFormsForm(forms.Form):

    brand = forms.CharField(max_length=48)
    price = forms.DecimalField(max_digits=16, decimal_places=0)
    size = forms.IntegerField(min_value=50)
    imageUrl = forms.URLField(label="Image URL:")

    brand.widget.attrs.update({"class": "form-control mb-3"})
    price.widget.attrs.update({"class": "form-control mb-3"})
    size.widget.attrs.update({"class": "form-control mb-3"})
    imageUrl.widget.attrs.update({"class": "form-control mb-3"})

  
# ----------------------------------------------------------------
# Views
# ----------------------------------------------------------------

# Listing all pianos
def index(request):
    # Annotate each Piano object with the count of upvotes (vote_type=1) 
    # and order the results alphabetically by brand.
    pianos = ( 
        Piano.objects.annotate(
        upvote_count=Count("piano_votes", filter=Q(piano_votes__vote_type=1))
        )
        .order_by("brand")
    )
    return render(request, "piano_app/index.html", {"pianos": pianos})


# Add a piano w/ ModelForm
@login_required
def add_piano(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
       
       # Populate the form with the request object
        form = CreatePianoForm(request.POST)
        
        # Server side validation
        if form.is_valid():
            # Don't commit yet because you need to take care of the foreign key
            piano = form.save(commit=False)
            #Add the user object as the foreign key reference
            piano.owner = user
            # Now save form and new model object
            piano.save()

            messages.success(request, "Your piano has been added.")

            # If successful, redirect
            return HttpResponseRedirect(reverse("index"))

        return render(request, "piano_app/add_piano.html", {"form": form})

    return render(request, "piano_app/add_piano.html", 
                  {"form": CreatePianoForm()})


# Add a piano Django forms
# Need to create and save the model instance
@login_required
def add_piano2(request):
    if request.method == "POST":
        # Binding data to the form
        form = CreatePianoFormsForm(request.POST)
        # Return user object of logged-in user
        user = User.objects.get(pk=request.user.id)
        # Extract data from bound form for new model object
        if form.is_valid():
            brand = form.cleaned_data["brand"]
            price = form.cleaned_data["price"]
            size = form.cleaned_data["size"]
            image = form.cleaned_data["imageUrl"]
            piano = Piano(
                brand=brand, 
                price=price, 
                size=size, 
                imageUrl=image,
                owner=user
                )
            piano.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "piano_app/add_piano2.html", 
                  {"form": CreatePianoFormsForm()})
    

# Add a piano functionality w/ HTML
@login_required
def add_piano1(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        brand = request.POST["brand"]
        price = request.POST["price"]
        size = request.POST["size"]
        url = request.POST["imageUrl"]
        new_piano = Piano(
                brand=brand, 
                price=price, 
                size=size, 
                imageUrl=url, 
                owner=user
                )
        try:
            new_piano.save()
        except IntegrityError:
            return render(request, "piano_app/add_piano1.html", 
                          {"msg": "Did not save piano"})
        return HttpResponseRedirect(reverse("index"))
    return render(request, "piano_app/add_piano1.html")


#View piano details
def piano_detail(request, piano_id):
    piano = get_object_or_404(Piano, pk=piano_id) 
    piano_votes = Vote.objects.filter(item=piano, vote_type=1).count() 
    last_user_vote = (Vote.objects.
                        filter(item=piano, voter=request.user)
                        .first()
                        )
    return render(request, "piano_app/piano_detail.html", 
                      {"piano": piano, 
                       "piano_votes": piano_votes,
                       "last_user_vote": last_user_vote})


# Asynchronous voting for a piano
@login_required
def vote(request, piano_id):
    if request.method == "PUT":
        try:
            # Convert JSON to python dictionary
            data = json.loads(request.body)
            vote_type = data.get("vote_type")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        if vote_type not in [-1, 1]:
            return JsonResponse({"error": "Incorrect vote type"}, status=400)
        
        piano = get_object_or_404(Piano, pk=piano_id)
        
        if request.user == piano.owner:
            return JsonResponse({"error": "Owner can't vote on own item"}, 
                                status=403)
        
        # Get or create the vote
        vote, created = Vote.objects.get_or_create(
            voter=request.user,
            item=piano,
            defaults={"vote_type": vote_type}
        )

        # If vote alredy exists
        if not created:
            if vote.vote_type == vote_type:
                # No change needed, return the current count
                vote_count = Vote.objects.filter(item=piano, vote_type=1).count()
                return JsonResponse({
                    "message": "Duplicate vote, vote total remains same", 
                    "vote_count": vote_count,
                    "vote_type": vote_type
                    })
            
            # Change vote type (upvote or downvote)
            vote.vote_type = vote_type
            vote.save()

        vote_count = Vote.objects.filter(item=piano, vote_type=1).count()
        message = "Vote updated" if not created else "Vote added"
        vote_count = vote_count

        return JsonResponse({
            "message": message,
            "vote_count": vote_count,
            "vote_type": vote_type
        })
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
        
        
@login_required
def delete_piano(request, piano_id):
    if request.method == 'DELETE':
        piano = get_object_or_404(Piano, id=piano_id)

        # Check if the current user is the piano owner
        if piano.owner.id != request.user.id:
            return HttpResponseForbidden("You don't have permission to delete this piano")

        piano.delete()
   
        return JsonResponse({"success": True, "message": "Piano deletion successfull"})
    # Returns a 405 method not allowed
    return HttpResponseNotAllowed(["DELETE"])


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        # email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "piano_app/login.html", {
                "message": "Invalid username and/or password."})
    else:
        return render(request, "piano_app/login.html")


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
            return render(request, "piano_app/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "piano_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "piano_app/register.html")

