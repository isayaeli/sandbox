from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Watchlist
# Register your models here.

admin.site.unregister(Group)
admin.site.site_header = 'SandBox Admin'

admin.site.register(Watchlist)


