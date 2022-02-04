from django.contrib import admin
from stocks.models import Symbol, Comment, Tag, Image

# Register your models here.
admin.site.register(Symbol)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Image)
