import uuid as uuid_lib

from django.db import models
from core.models import TimeStampModel
from profiles.models import Profile


class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=False, blank=False, upload_to='images')

    def __str__(self):
        return self.name


class Tag(models.Model):
    slug = models.SlugField(max_length=225, unique=True)
    name = models.CharField(max_length=50, unique=True)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# class Industry(models.Model):
#     slug = models.SlugField(max_length=225, unique=True)
#     name = models.CharField(max_length=100)
#     image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL))

#     def __str__(self);
#     return self.name


# class Sector(models.Model):
#     slug = models.SlugField(max_length=225, unique=True)
#     name = models.CharField(max_length=100)
#     image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL))

#     def __str__(self);
#     return self.name


class Symbol(TimeStampModel):
    slug = models.SlugField(max_length=225, unique=True)
    symbol = models.CharField(max_length=20, blank=False)
    image = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=100, blank=False)
    currency = models.CharField(max_length=10, blank=True)
    symbol_type = models.CharField(max_length=50, blank=True)
    exchange = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    photo = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)
    # mic = models.ForeignKey()
    vender = models.CharField(max_length=3, blank=False)
    tags = models.ManyToManyField(Tag, blank=True)
    voters = models.ManyToManyField(Profile, related_name="like", through="FavoriteSymbol")

    def __str__(self):
        return f'{self.symbol}'


class FavoriteSymbol(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile','symbol'],  name="unique_symbols")
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.profile.user.username} likes {self.symbol.symbol}'


class Comment(TimeStampModel):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, primary_key=True, unique=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    symbols = models.ManyToManyField(Symbol, related_name='comments', blank=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='reply_comment')
    likes = models.ManyToManyField(Profile, related_name='comment_like', blank=True)
    # trade = models.ForeignKey()
    body = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.uuid)


class KeyMetric(TimeStampModel):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    changes = models.FloatField(null=True, blank=True)
    cap =  models.BigIntegerField(null=True, blank=True)
    peRatio = models.FloatField(null=True, blank=True)
    opGrowth = models.FloatField(null=True, blank=True)
    roe = models.FloatField(null=True, blank=True)
    deRation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.symbol.symbol} created by {self.created_at}'
