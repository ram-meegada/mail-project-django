from rest_framework import serializers
from .models import *

class TokenAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenAmountModel
        fields = "__all__"

class SendMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMail
        fields = "__all__"

class EmailFilteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailFilteringModel 
        fields = ['id', 'subject', 'body', 'category']             

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['email','password','username', 'first_name', 'last_name']
        extra_kwargs = {"password": {"write_only":True}}        