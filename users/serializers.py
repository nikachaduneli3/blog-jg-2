from django.template.context_processors import request
from rest_framework import serializers
from .models import User



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)
    gender = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('passwords didn\'t match!')
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture',
                  'gender', 'first_name', 'last_name']

