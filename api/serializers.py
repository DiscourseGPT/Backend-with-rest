from rest_framework import serializers
from .models import Profile
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'