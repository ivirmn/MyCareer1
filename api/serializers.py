from rest_framework import serializers
from MyCareer.models import UserProfile, Demand


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = "__all__"
