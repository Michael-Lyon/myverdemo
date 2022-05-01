from hashid_field import Hashid
from django.utils.timezone import now
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MyUser, Profile
from rest_framework.authtoken.models import Token
from utils.generate import get_keys
from django.conf import settings
from hashid_field import Hashid
from hashid_field.rest import HashidSerializerCharField

User = settings.AUTH_USER_MODEL


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    profile = ProfileSerializer(required=True)
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        # fields = '__all__'
        fields = ('id', 'first_name', 'username', 'last_name', 'password',
                  'email', 'days_since_joined', 'profile')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        otp = validated_data.pop('otp')
        print(validated_data)
        user = MyUser.objects.create_user(**validated_data)
        profile = Profile.objects.create(user=user, otp=otp ,ref_code=get_keys(5), **profile_data)
        profile.save()
        user.save()

        return user

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days

    def get_id(self, obj):
        id = obj.id
        return id

   


