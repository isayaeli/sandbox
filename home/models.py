from django.db import models


class Watchlist(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    career_background = models.CharField(max_length=100)


    def __str__(self):
        return self.full_name