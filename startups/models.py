from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import opportunity


class Startup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name  =  models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    logo =  models.FileField(upload_to='startup_images')
    registered_on = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=100,null=True, blank=True)
    size = models.CharField(max_length=100,null=True, blank=True)
    website = models.URLField(max_length=100,null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    what_we_offer = models.TextField(null=True, blank=True)
    description = models.TextField()
    def __str__(self):
        return str(self.user)

    @property
    def get_rating(self):
        rating = Startup_Rating.objects.filter(rating_for=self.id)

        sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

        all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
        try:
            rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
        except ZeroDivisionError:
            rates = 0
        return rates
      

    @property
    def get_required_skills(name):
        skill = Skills_Required.objects.filter(startup=name)
        return skill
    
    @property
    def get_opportunities(name):
        opp = opportunity.models.Opportunity.objects.filter(startup_name=name)
        return opp
    




class Skills_Required(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)


    def __str__(self):
        return self.skill

    class Meta:
        verbose_name_plural = "Skills_Required"



class Startup_Rating(models.Model):
    rating_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_for =  models.ForeignKey(Startup, on_delete=models.CASCADE)
    rating_date = models.DateTimeField(default=datetime.now)
    rating_value = models.FloatField(max_length=100)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rating_for)


