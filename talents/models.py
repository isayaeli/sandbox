from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from hitcount.models import  HitCount
from django.contrib.contenttypes.fields import GenericRelation
import dashboard



# Create your models here.


SECTORS = (
    ('Architecture & Construction','Architecture & Construction'),
    ('Accountancy and Financial Management','Accountancy and Financial Management'),
    ('Business, Consulting and Management','Business, Consulting and Management '),
    ('Law and Legal Services','Law and Legal Services'),
    ('Non Government Organization','Non Government Organization '),
    ('Media and Communications','Media and Communications'),
    ('Creative Arts and Design','Creative Arts and Design'),
    ('Energy and Utilities','Energy and Utilities'),
    ('Engineering and Manufacturing','Engineering and Manufacturing'),
    ('Agribusiness','Agribusiness'),
    ('Medical and Healthcare','Medical and Healthcare'),
    ('Information Technology','Information Technology'),
    ('Hospitality and Tourism','Hospitality and Tourism'),
    ('Marketing, Advertising and PR','Marketing, Advertising and PR'),
    ('Sales','Sales'),
    ('Real Estate','Real Estate'),
    ('Finance, Retail and Banking Services','Finance, Retail and Banking Services'),
    ('Office Management and Human Resources Services','Office Management and Human Resources Services'),
    ('Transportation, Distribution & Logistics','Transportation, Distribution & Logistics')
)

WORK_EXP =(
    ('Less than 1 Year', 'Less than 1 Year'),
    ('2-5 years','2-5 years'),
    ('5-7 years','5-7 years'),
    ('7-10 years', '7-10 years'),
    ('10 years and above', '10 years and above')      
)
GENDER = (
    ('male','male'),
    ('female','female'),
)
JOB_CATEGORIES = (
    ('full time', 'full time'),
    ('remote', 'remote'),
    ('contractual','contractual'),
    ('internship','internship'),
    ('voluntering', 'voluntering'),
    ('freelance','freelance'),
    ('part-time','part-time'),
    ('temporary', 'temporary'),
    ('internship','internship')
)


class Talent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(User, related_name="views", blank=True)
    profession  = models.CharField(max_length=100)
    about = models.TextField()
    category = models.CharField(max_length=100, choices=SECTORS)
    years_of_experience = models.CharField(max_length=100, choices=WORK_EXP)
    dob = models.DateTimeField(default=datetime.now)
    gender = models.CharField(max_length=10, choices=GENDER)
    languages = models.CharField(max_length=100)
    salary_expectation = models.CharField(max_length=100)
    prefered_work_type = models.CharField(max_length=100,choices=JOB_CATEGORIES)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    linkedIn = models.URLField(null=True, blank=True)
    slug = models.SlugField(default=User, unique=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Talent, self).save(*args, **kwargs)

    @property
    def get_skills(user):
        skills = Skill.objects.filter(talent=user)
        return skills
    
    
    @property
    def get_experience(user):
        exp = Experience.objects.filter(talent=user)
        return exp
    
    @property
    def get_education(user):
        edu = Education.objects.filter(talent=user)
        return edu
    
    @property
    def get_award(user):
        awd = Award.objects.filter(talent=user)
        return awd

    
    @property
    def get_rating(self):
        rating =dashboard.models.Rating.objects.filter(rating_for=self.id)

        sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

        all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
        try:
            rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
        except ZeroDivisionError:
            rates = 0
        return rates

    def __str__(self):
        return self.user.username



# def create_talent(sender, **kwargs):
#     if kwargs['created']:
#        talent = Talent.objects.create(user=kwargs['instance'])
       
# post_save.connect(create_talent, sender=User)


class Experience(models.Model):
    WORKING = (
        ('No','No'),
        ('Yes',"Yes")
    )
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    company_name =  models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    finish_date = models.DateTimeField(null=True, blank=True)
    still_working = models.CharField(max_length=100, null=True,blank=True, choices=WORKING)
    position = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return str(self.talent)


class Education(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    speciality =  models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(max_length=100)
    school_name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return str(self.talent)
    
    class Meta:
        verbose_name_plural = 'Education'
    

class Award(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    name =  models.CharField(max_length=100)
    awarded_on = models.DateTimeField(default=datetime.now)
    details = models.TextField()

    def __str__(self):
        return str(self.talent)

class Skill(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    experience = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return str(self.talent)



