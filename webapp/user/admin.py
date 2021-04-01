from django.contrib import admin

# Register your models here.
from user.models import account,user
admin.site.register(account)
admin.site.register(user)
