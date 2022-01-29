from django.db import models
from core.models import TimeStampModel
from profiles.models import Profile


class Symbol(TimeStampModel):
    slug = models.SlugField(max_length=225, unique=True)
    symbol = models.CharField(max_length=20, blank=False)
    description = models.CharField(max_length=100, blank=False)
    currency = models.CharField(max_length=10, blank=True)
    symbol_type = models.CharField(max_length=50, blank=True)
    exchange = models.CharField(max_length=100, blank=True)
    # mic = models.ForeignKey()
    vender = models.CharField(max_length=3, blank=False)
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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.body} by {self.author.user.username}'
