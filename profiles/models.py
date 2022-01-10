import uuid as uuid_lib

from django.db import models
from django.conf import settings
from core.models import TimeStampModel


# Create your models here.
class Profile(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    # following = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserFollowing')

    def __str__(self):
        return self.user.username


# class UserFollowing(models.Model):
#     following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='me')
#     created_at = models.DateTimeField(auto_now_add=True)


class FavoStock(TimeStampModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
    symbol = models.CharField(max_length=20, blank=False)
    isin = models.CharField(max_length=12, blank=True)
    vender = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"{self.profile.user.username} likes {self.symbol}"

