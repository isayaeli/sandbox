import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from opportunity.models import Opportunity
from .models import Watchlist
from talents.models import Talent
from startups.models import Startup
from dashboard.models import Listing, Package_Payment, Matches


# Create your views here.

def home(request):
    opportunities = Opportunity.objects.all().order_by('-id')[:9]
    startups =  Startup.objects.all().order_by('-id')[:10]
    listings = Listing.objects.all()
    talents = Talent.objects.all()
    matches = Matches.objects.all()

    package = ''
    if request.user.is_authenticated:
       package =  Package_Payment.objects.filter(user=request.user).last()
    
    
    context = {
        'opportunities':opportunities,
        'startups':startups,
        'listings':listings,
        'package':package,
        'talents':talents,
        'matches':matches
        
    }
    return render(request, 'home/home.html', context)


def watchlist(request):
    if request.method == 'POST':
        full_name = request.POST['name']
        email = request.POST['email']
        profession = request.POST['prof']
        location = request.POST['location']
        career_background = request.POST['career']
        response_data = {}
        watchlist= Watchlist(full_name=full_name, email=email, profession=profession,
         location=location,career_background=career_background)
        watchlist.save()
        response_data['success'] = "Information has been succesful submited"
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
      
    return redirect('landing')


def about(request):
    return render(request, 'home/about.html')

def contacts(request):
    return render(request, 'home/contacts.html')


def landing(request):
    return render(request, 'landing/home.html')


def lms_home(request):
    return render(request, 'home/lms_home.html')



def handler404(request, exception):
    return render(request, 'errors/404.html', locals())

def terms_conditions(request):
    return render(request, 'home/terms_conditions.html')

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')


def how_it_works(request):
    return render(request, 'home/how_it_works.html')