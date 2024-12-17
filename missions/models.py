from django.db import models
from spy_cats.models import Cats


class Missions(models.Model):
    cat = models.ForeignKey(Cats, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)

    def __repr__(self):
        return self.id


class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    mission = models.ForeignKey(Missions, on_delete=models.CASCADE)

    def __repr__(self):
        return self.name
