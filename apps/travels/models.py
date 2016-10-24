from __future__ import unicode_literals

from django.db import models
from ..users.models import User

from datetime import datetime

# Create your models here.

class TravelManager(models.Manager):
    def make_trip(self, destination, description, planner_id, start_date, end_date):
        errors = []
        if destination == "":
            errors.append("Destination may not be empty")
        if description == "":
            errors.append("Description may not be empty")
        if start_date == "":
            errors.append("Start Date may not be empty")
        if end_date == "":
            errors.append("End Date may not be empty")
        elif start_date != "":
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            if start > end:
                errors.append("End Date must not be before Start Date")
            if start < datetime.now().date():
                errors.append("Start Date may not be in the past")
            if end < datetime.now().date():
                errors.append("End Date may not be in the past")
        trip = None;
        if len(errors) == 0:
            trip = Trip(destination=destination, description=description, planner = User.objects.get(id=planner_id), start_date=start, end_date=end)
            trip.save()
        return (trip, errors)

    def get_unjoined_trips(self, traveller_id):
        traveller = User.objects.get(id=traveller_id)
        try:
            joined = Trip.objects.filter(planner=traveller).values_list("id", flat=True) | traveller.joined_trips.all().values_list("id", flat=True)
            return self.exclude(id__in=joined)
        except ValueError:
            return self.all()

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField(max_length = 10000)
    planner = models.ForeignKey(User, related_name = "planned_trips")
    start_date = models.DateField()
    end_date = models.DateField()
    travellers = models.ManyToManyField(User, related_name = "joined_trips", blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TravelManager()

    def join_trip(self, joiner_id):
        joiner = User.objects.get(id=joiner_id)
        if (joiner == self.planner) | (joiner in self.travellers.all()):
            return False
        self.travellers.add(joiner)
        return True
