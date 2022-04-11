import imp
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
import json
from django.contrib import messages


from userauth.models import Profile
from .models import Opportunity
from dashboard.models import Matches
from talents.models import Talent
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def opportunity(request):
    opportunities = Opportunity.objects.all().order_by('-id')
    opportunities_count = opportunities.count()

    startup = Profile.objects.filter(user_type='startup')[:3]

    qs = request.GET.get('q')
    qs2 =  request.GET.get('search')
    if qs:
        opportunities = Opportunity.objects.filter(
            Q(category__icontains=qs)|
            Q(experience__icontains=qs)|
            Q(salary_range__icontains=qs)|
            Q(title__icontains=qs)|
            # Q(startup_name=qs)|
            Q(location__icontains=qs)|
            Q(sector__icontains=qs)).order_by('-id')

    elif qs2:
        opportunities = Opportunity.objects.filter(
            Q(title__icontains=qs2)and
            Q(location__icontains=qs2)).order_by('-id')


    page = request.GET.get('page', 1)
    paginator = Paginator(opportunities, 8)
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps =paginator.page(paginator.num_pages)
    
    context = {
        'opportunities':opportunities,
        'opportunities_count':opportunities_count,
        'opps':opps,
        'startup':startup
    }
    return render(request, 'opportunity/opportunity.html', context)



def opportunity_details(request, id):
    opportunity = Opportunity.objects.get(id=id)
    all_opportunities = Opportunity.objects.all().order_by('-id')[:5]
    opportunities =  Opportunity.objects.filter(user=opportunity.user).order_by('-id')[:4]

    context = {
        'data':opportunity,
        'opportunities':opportunities,
        'all':all_opportunities
    }
    
    return render(request, 'opportunity/opp_details.html', context)


def add_match(request):
    talent = Talent.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        startup = request.POST.get('the_startup')
        opportunity = request.POST.get('the_opp')
        response_data = {}
        matched = Matches.objects.filter(user=request.user,opportunity=opportunity )
        if matched.exists():
            response_data['result'] = "You have already matched this opportunity."
            return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json")
        else:
            matches = Matches(startup_id=startup, user=request.user, talent=talent)
        matches.save()
        matches.opportunity.add(opportunity)
        
        response_data['result'] = "Match submited"
        # response_data['opp_id'] = matches.id
        # response_data['startup'] = matches.startup
        # response_data['opp_title'] = matches.opportunity_title
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({'Error':'Faild to submit'}),
            content_type = "application/json"
        )


def remove_match(request, id):
    match = Matches.objects.get(id=id)
    match.delete()
    messages.success(request, 'Successful Deleted your match')
    return redirect('talent_dash')




def mark(request):
    if request.method == 'POST':
        opp = Opportunity.objects.get(id=request.POST.get('id'))
        is_marked = False
        if opp.marked.filter(id=request.user.id).exists():
            opp.marked.remove(request.user)
            is_marked = False
        else:
            opp.marked.add(request.user)
            is_marked = True


        response_data = {}
        response_data['result'] = 'Successfull marked'
        response_data['is_marked']= is_marked
        response_data['the_id'] = opp.id
        return HttpResponse(
            json.dumps(response_data),
            content_type='applicatin/json'
        )
    else:
        return HttpResponse(
            json.dumps({'Error':'Faild to submit'}),
            content_type = "application/json"
        )
