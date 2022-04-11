from django.contrib import admin
from .models import Matches, Message, Thread, Rating, Package_Payment, Listing
# Register your models here.

admin.site.register(Matches)
admin.site.register(Rating)
admin.site.register(Package_Payment)
admin.site.register(Listing)


class Mesaages(admin.TabularInline):
    model = Message


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        Mesaages,
    ]

    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)