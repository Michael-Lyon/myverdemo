from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
import json
from rest_framework import serializers
from django.forms import ValidationError
from django.shortcuts import render
from accounts.serializers import UserSerializer
from utils.generate import get_keys
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import MyUser, Profile
from rest_framework.authtoken.models import Token
from rest_framework import generics
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
# Create your views here.


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
            posted_data = self.request.data

            queryset = MyUser.objects.filter(email=posted_data['email'])
            if queryset.exists():
                # raise ValidationError('You have already signed up')
                raise serializers.ValidationError({"email":"This email is already in use."})
            else:
                try:
                    first_name = posted_data["first_name"]
                    code = get_keys(6)
                    phone= posted_data['profile']["phone_number"]

                    account_sid = os.environ['TWILIO_ACCOUNT_SID']
                    auth_token = os.environ['TWILIO_AUTH_TOKEN']
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        to="+2347068733754",
                        # from_="+23467101616",
                        from_=os.environ['FROM_NUM'],
                        body=f"Hi your otp is {code}"
                    )
                    

                    print(message.sid, message.status)
                    serializer.save(otp=code)
                except TwilioRestException as exc:
                    # print(exc)
                    raise serializers.ValidationError({"error":f"{exc.msg} (code: {exc.code})"})


@api_view(["POST"])
def login_user(request):
    data = {}
    reqBody = json.loads(request.body)
    email1 = reqBody['email']

    print(email1)
    password = reqBody['password']
    try:

        Account = MyUser.objects.get(email=email1)
    except BaseException as e:
        return Response({"message": "user doesnt exist"})
        # raise ValidationError({"400": f'{str(e)}'})



    token = Token.objects.get_or_create(user=Account)[0].key
    # print(token)
    if not check_password(password, Account.password):
        return Response({"message": "Incorrect Login credentials"})
        # raise ValidationError({"message": "Incorrect Login credentials"})

    if Account:
        if Account.is_active:
            login(request, Account)
            data["message"] = "user logged in"
            data["user"] = Account.id
            data["email"] = Account.email

            Res = {"data": data, "token": token}
            return Response(Res)
        else:
            return Response({"message": 'Account not active'})
    else:
        return Response({"message": 'Account doesnt exist'})
