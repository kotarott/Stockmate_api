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
    followees = models.ManyToManyField('self', through='FriendShip', symmetrical=False, related_name='+',
                                       through_fields=('follower', 'followee'), verbose_name='フォロー中')
    followers = models.ManyToManyField('self', through='FriendShip', symmetrical=False, related_name='+',
                                       through_fields=('followee', 'follower'), verbose_name='フォロワー')

    def __str__(self):
        return self.user.username


class FriendShip(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followee_friendships')
    followee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_friendships')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower','followee'],  name="unique_followers")
        ]
        ordering = ["-created_at"]
    
    def __str__(self):
        return f'{self.follower.user.username} follows {self.followee.user.username}'


# class FavoStock(TimeStampModel):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
#     symbol = models.CharField(max_length=20, blank=False)
#     vender = models.CharField(max_length=10, blank=True)
#     description = models.CharField(max_length=100, blank=False)

#     def __str__(self):
#         return f"{self.profile.user.username} likes {self.symbol}"

