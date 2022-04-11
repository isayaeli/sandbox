import json
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Startup, Startup_Rating
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from .forms import ratingForm
# Create your views here.

def startups(request):
    startups = Startup.objects.all().order_by('-id')
    startup_count = startups.count()

    qs = request.GET.get('q')
    if qs:
        startups = Startup.objects.filter(
            Q(name__icontains=qs)|
            Q(size__icontains=qs)|
            Q(location__icontains=qs)|
            Q(description__icontains=qs)|
            # Q(skill__icontains=qs)|
            Q(category__icontains=qs)).order_by('-id')
        
    page = request.GET.get('page', 1)
    paginator = Paginator(startups, 8)
    try:
        startup = paginator.page(page)
    except PageNotAnInteger:
        startup = paginator.page(1)
    except EmptyPage:
        startup =paginator.page(paginator.num_pages)
    context = {
        'startups':startups,
        'startup':startup,
        'startup_count':startup_count,
        
    }
    return render(request, 'startups/startups.html', context)


def startup_details(request, id):
    startup = get_object_or_404(Startup, id=id)

    rating = Startup_Rating.objects.filter(rating_for=startup.id)
    sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

    all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
    try:
       rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0
    
    context = {
        'data':startup,
        'rates':rates
    }

    hit_count = get_hitcount_model().objects.get_for_object(startup)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    return render(request, 'startups/startupDetails.html',context)



def follow(request):
    if request.method == 'POST':
        startup = get_object_or_404(Startup, id=request.POST.get('id'))
        is_followed = False
        if startup.followers.filter(id=request.user.id).exists():
            startup.followers.remove(request.user)
            is_followed = False
        else:
            startup.followers.add(request.user)
            is_followed = True

        followers_count = startup.followers.all().count()
        response_data = {}
        response_data['result'] = 'Successfull followed'
        response_data['is_followed']= is_followed
        response_data['the_id'] = startup.id
        response_data['count'] = followers_count
        return HttpResponse(
            json.dumps(response_data),
            content_type='applicatin/json'
        )
    else:
        return HttpResponse(
            json.dumps({'Error':'Faild to submit'}),
            content_type = "application/json"
        )




def rate(request, id):
    if request.method == 'POST':
        form = ratingForm(request.POST or None)
        print(request.POST)
        rating = Startup_Rating()
        if form.is_valid():
            rating.rating_by = request.user
            rating.rating_for_id = form.cleaned_data['rating_for']
            rating.rating_value = form.cleaned_data['ratings']
            rating.comments = form.cleaned_data['comments']
            rating.save()
            return redirect('startup_details',id=id)
        # return redirect('/')
            
    return redirect('startup_details',id=id)

    



    # CRO-IUdq-I5Dl-VuQ9h