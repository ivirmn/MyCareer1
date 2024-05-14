from rest_framework import serializers
from MyCareer.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'firstname', 'surname', 'patronymic')
