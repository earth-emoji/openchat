from rest_framework import serializers

from .models import UserProfile
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'slug')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('user', 'slug', 'contacts')