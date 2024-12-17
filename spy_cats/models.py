from django.db import models


class Cats(models.Model):
    name = models.CharField(max_length=100)  # Cats Name
    year_of_exp = models.FloatField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __repr__(self):
        return self.name
