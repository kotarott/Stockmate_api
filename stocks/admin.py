from django.contrib import admin
from stocks.models import Symbol, Comment

# Register your models here.
admin.site.register(Symbol)
admin.site.register(Comment)