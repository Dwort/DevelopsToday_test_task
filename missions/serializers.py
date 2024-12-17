from rest_framework import serializers
from .models import Missions, Target, Cats


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'complete']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, write_only=True)
    cat_name = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    cat = serializers.CharField(source='cat.name', read_only=True)

    class Meta:
        model = Missions
        fields = ['id', 'cat_name', 'cat', 'notes', 'complete', 'targets']

    def validate_cat_name(self, value):
        if value in [None, ""]:
            return None

        try:
            cat = Cats.objects.get(name=value)
        except Cats.DoesNotExist:
            raise serializers.ValidationError("Cat with this name does not exist.")

        if Missions.objects.filter(cat=cat).exists():
            raise serializers.ValidationError("This cat already has an active mission.")
        return value

    def validate_targets(self, value):
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError("Targets count must be between 1 and 3.")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        cat_name = validated_data.pop('cat_name', None)

        cat = None
        if cat_name:
            cat = Cats.objects.get(name=cat_name)

        mission = Missions.objects.create(cat=cat, **validated_data)

        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)

        return mission

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['targets'] = TargetSerializer(instance.target_set.all(), many=True).data
        return representation
