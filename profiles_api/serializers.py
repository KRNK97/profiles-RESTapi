from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIview"""
    name = serializers.CharField(max_length=10)

# this serializer will be based on Model Serializer class


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ("id", "email", "name", "password")
        # we need to modify the password field
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # overwrite the create method
    def create(self, validated_data):
        """create and return new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on",)

        # user profile will be logged in used, we set it from views.py
        extra_kwargs = {
            "user_profile": {
                "read_only": True
            }
        }
