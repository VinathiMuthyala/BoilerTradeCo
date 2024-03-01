from rest_framework import serializers
from .models import Profile

class AppSerializer (serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'avatar']
