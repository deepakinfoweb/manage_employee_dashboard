from django.db import models
from datetime import datetime,timedelta
import uuid
from rest_framework import serializers

class account(models.Model):
    account_id = models.AutoField(primary_key=True) #1=> Active, 2=> inactive
    account_name = models.CharField(max_length =100, default = None, null=False)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.account_id)

class user(models.Model):
    profile_id  = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False)
    phone_id=models.IntegerField(null=False, blank=False,unique=True)
    email = models.CharField(max_length=100, blank=False)
    photo = models.ImageField(upload_to='images/')
    account_type = models.ForeignKey(account, on_delete=models.CASCADE, default = 1)
    status =  models.CharField(max_length=100, default='Pending')
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.profile_id)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
