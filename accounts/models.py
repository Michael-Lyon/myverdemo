from utils.generate import get_keys
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import reverse
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.fields import DateTimeField
from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser
from hashid_field import HashidAutoField


class MyUser(AbstractUser):
    id = HashidAutoField(primary_key=True)


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True, blank=True) 
    phone_number = models.CharField(max_length=15)
    ref_code = models.CharField(max_length=15, blank=True, null=True)
    recomended_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    signup_confirmation = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        my_recs = []
        for profile in qs:
            try:
                if profile.recomended_by == self.user:
                    my_recs.append(profile.user.username)
            except Exception as e:
                pass
        return my_recs
