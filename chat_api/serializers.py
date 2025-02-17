from rest_framework import serializers
from .models import User, Chat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'tokens']
        extra_kwargs = {'password': {'write_only': True}}

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'tokens', 'auth_token']
        extra_kwargs = {
            'auth_token': {'read_only': True},
            'tokens': {'read_only': True}
        }

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'message', 'response', 'timestamp']