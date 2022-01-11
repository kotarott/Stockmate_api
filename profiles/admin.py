from django.contrib import admin
from profiles.models import Profile, FavoStock, FriendShip

# Register your models here.
admin.site.register(Profile)
admin.site.register(FavoStock)
admin.site.register(FriendShip)