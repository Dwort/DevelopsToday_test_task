from rest_framework import serializers
from .models import Cats


class CatRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cats
        fields = ['id', 'name', 'year_of_exp', 'breed', 'salary']


class CatSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cats
        fields = ['salary']
