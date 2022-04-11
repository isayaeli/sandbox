from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from talents.models import Talent
from opportunity.models import Opportunity
from startups.models import Startup



# Create your models here.


STATUS = (
        ('shortlisted','shortlisted'),
        ('rejected','rejected'),
        ('reviewing','reviewing'),
        ('interviewed','interviewed'),
        ('offergiven','offergiven')
    )
class Matches(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matched_on = models.DateTimeField(default=datetime.now)
    status = models.CharField(choices=STATUS, max_length=100, default='reviewing')
    opportunity= models.ManyToManyField(Opportunity)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, null=True, blank=True)
    startup = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return str(self.user)
    

    class Meta:
        verbose_name_plural = 'Matches'

    @property
    def get_rating(self):
        rating = Rating.objects.filter(rating_for=self.talent)

        sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

        all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
        try:
            rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
        except ZeroDivisionError:
            rates = 0
        return rates


    


class Thread(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{str( self.sender)} and {str( self.reciever)}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True)
    user        = models.ForeignKey(User, verbose_name='sender', null=True, on_delete=models.CASCADE)
    the_message = models.TextField()
    sent_on = models.DateTimeField(default=datetime.now)

    # def __str__(self):
    #     return f"{str( self.thread.sender)},{str( self.thread.reciever)}"



class Rating(models.Model):
    rating_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_for =  models.ForeignKey(Talent, on_delete=models.CASCADE)
    rating_date = models.DateTimeField(default=datetime.now)
    rating_value = models.FloatField(max_length=100)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rating_for)


class Package_Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package_name = models.ForeignKey('Listing', on_delete=models.CASCADE, null=True)
    posted_opportunity = models.IntegerField()
    amount_paid = models.CharField(max_length=100)
    txt_ref = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    date_paid = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.user.username
    

CHOICES = (
    ('Yes','Yes'),
     ('No','No')
)
class Listing(models.Model):
    name = models.CharField(max_length=100)
    charge = models.CharField(max_length=100, default=0)
    opportunity_listing = models.CharField(max_length=100,choices=CHOICES, default='No')
    talent_due_deligency = models.CharField(max_length=100, choices=CHOICES, default='No')
    legal = models.CharField(max_length=100,choices=CHOICES, default='No')
    payroll = models.CharField(max_length=100,choices=CHOICES, default='No')

    def __str__(self):
        return self.name



