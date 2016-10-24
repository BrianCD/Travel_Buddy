from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages

from models import *

# Create your views here.
def index(response):
    if "user" not in response.session:
        messages.error(response, "You are not logged in!")
        return redirect("/")
    user = User.objects.get(id=response.session["user"]["id"])
    return render(response, "travels/index.html", {"trips":list(Trip.objects.filter(planner=user)) + list(user.joined_trips.all()), "others":Trip.objects.get_unjoined_trips(user.id), "user":user})

def display_trip(response, trip_id):
    if "user" not in response.session:
        messages.error(response, "You are not logged in!")
        return redirect("/")
    trip = Trip.objects.get(id=trip_id)
    return render(response, "travels/trip.html", {"trip":trip})

def add_trip(response):
    if "user" not in response.session:
        messages.error(response, "You are not logged in!")
        return redirect("/")
    messagelist = messages.get_messages(response).__iter__()
    try:
        header = messagelist.next()
    except StopIteration:
        header = ""
    rest = []
    for message in messagelist:
        rest.append(message)
    return render(response, "travels/add.html", {"header":header, "rest":rest})

def join_trip(response, trip_id):
    if "user" not in response.session:
        messages.error(response, "You are not logged in!")
        return redirect("/")
    trip = Trip.objects.get(id=trip_id)
    if trip.join_trip(response.session["user"]["id"]):
        messages.success(response, "Successfully registered!")
    else:
        messages.error(response, "You are already on that trip!")
    return redirect("/travels/")

def new_trip(response):
    if "user" not in response.session:
        messages.error(response, "You are not logged in!")
        return redirect("/")
    post = response.POST
    result = Trip.objects.make_trip(post["destination"], post["description"], response.session["user"]["id"], post["start_date"], post["end_date"])
    if result[0] is None:
        messages.error(response, "You have errors in your trip:")
        for error in result[1]:
            messages.error(response, error)
        return redirect("/travels/add")
    messages.success(response, "Successfully created trip!")
    return redirect("/travels/")
