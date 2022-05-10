import math, random
from django.http.response import HttpResponse, JsonResponse
import json
import requests
from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from opportunity.models import Opportunity
from .forms import *
from talents.models import Talent, Education, Skill
from .models import Matches, Message, Thread, Rating, Package_Payment, Listing
from startups.models import Startup_Rating ,Startup
from datetime import datetime
from django.conf import settings



# Create your views here.
@login_required(login_url='/auth')
def dash(request):
    opportunities = Opportunity.objects.filter(user=request.user).order_by('-id')[:5]
    opportunities_count = Opportunity.objects.filter(user=request.user).count()
    
    expired = Opportunity.objects.filter(user=request.user, deadline__lt=datetime.now()).count()
    active = Opportunity.objects.filter(user=request.user, deadline__gte=datetime.now()).count()

    matches = Matches.objects.filter(startup=request.user.id).order_by('-id')
    matches_count = Matches.objects.filter(startup=request.user.id).count()

    startup =  Startup.objects.get(user=request.user)
    startup_rating =  Startup_Rating.objects.filter(rating_for=startup)


    shortlisted_number = matches.filter(status='shortlisted').count()
    try:
        shortlisted_pcnt = round(shortlisted_number / matches_count * 100, 1)
    except ZeroDivisionError:
        shortlisted_pcnt = 0
  

    interviewed_number = matches.filter(status='interviewed').count()
    try:
        interviewed_pcnt = round(interviewed_number / matches_count * 100, 1)
    except ZeroDivisionError:
        interviewed_pcnt = 0

    offer_number = matches.filter(status='offergiven').count() 
    total_contacted = (interviewed_number + shortlisted_number + offer_number)
    try:
        contacted_pcnt = round(total_contacted / matches_count * 100, 1)
    except ZeroDivisionError:
        contacted_pcnt = 0
    

    context = {
        'opportunities':opportunities,
        'opportunities_count':opportunities_count,
        'matches':matches,
        'matches_count':matches_count,
        'startup_rating':startup_rating,
        'data':startup, 
        'is_expired':expired,
        'active':active,

        'shortlisted_number':shortlisted_number,
        'shortlisted_pcnt':shortlisted_pcnt,

        'interviewed_number':interviewed_number,
        'interviewed_pcnt':interviewed_pcnt,

        'total_contacted':total_contacted,
        'contacted_pcnt':contacted_pcnt

    }

    return render(request, 'dash/home.html', context)

@login_required(login_url='/auth')
def packages(request):
    package =  Package_Payment.objects.filter(user=request.user).last()
    listings = Listing.objects.all()
    tx_ref = ''+str(math.floor(1000000 + random.random()*9000000)),
    if request.method == 'POST':
        print(request.POST)
        pays = Package_Payment()
        form =  paymentForm(request.POST)
        if form.is_valid():
            pays.user = request.user
            pays.txt_ref = tx_ref
            pays.package_name_id = form.cleaned_data['listing_name']
            pays.posted_opportunity = form.cleaned_data['posted_opportunity']
            if form.cleaned_data['pack_name'] == 'Basic':
                pays.amount_paid = 10 * int(form.cleaned_data['posted_opportunity'])
            elif form.cleaned_data['pack_name'] == 'Advanced':
                pays.amount_paid = 40 * int(form.cleaned_data['posted_opportunity'])
            elif form.cleaned_data['pack_name'] == 'Premium':
                pays.amount_paid = 110 * int(form.cleaned_data['posted_opportunity'])
            pays.save()

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            if form.cleaned_data['pack_name'] == 'Basic':
                amount = int(form.cleaned_data['posted_opportunity']) * 10
            elif form.cleaned_data['pack_name'] == 'Advanced':
               amount = int(form.cleaned_data['posted_opportunity']) * 40
            elif form.cleaned_data['pack_name'] == 'Premium':
                amount = int(form.cleaned_data['posted_opportunity']) * 110
            phone = form.cleaned_data['phone']
           
            
            messages.success(request, f'Successful paid for listing package')
            return redirect(str(process_payment(name,email,amount,phone, tx_ref)))
        messages.error(request, f"error occured while submitting a form")
        return redirect('packs')
    context = {
        'package':package,
        'listings':listings
    }
    return render(request, 'dash/packs.html', context)


def process_payment(name,email,amount,phone, tx_ref):
     auth_token= settings.RAVE_SECRET_KEY
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":tx_ref,
                "amount":amount,
                "currency":"TZS",
                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"card, ussd",
                # "meta":{
                #     "consumer_id":customer_id,
                #     "consumer_mac":"92a3-912ba-1192a"
                # },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Plumar",
                    "description":"The best talent recruitment in town",
                    "logo":"http://localhost:8000/static/assets/img/fav.png"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link


from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    package =  Package_Payment.objects.filter(user=request.user).last()
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    
    # print(status)
    # print(tx_ref)

    if package.txt_ref == tx_ref and status == 'successful':
        package.verified = True
        package.save()

    context = {
        'status':status,
        'tx_ref':tx_ref
    }
    return render(request, 'dash/success.html', context)


def zoom(request):
    return render(request, 'dash/zoom.html')


def ats(request):
    matches = Matches.objects.filter(startup=request.user.id).order_by('-id')
    matches_count = Matches.objects.filter(startup=request.user.id).count()

    shortlisted_number = matches.filter(status='shortlisted').count()
    try:
        shortlisted_pcnt = round(shortlisted_number / matches_count * 100, 1)
    except ZeroDivisionError:
        shortlisted_pcnt = 0
  

    interviewed_number = matches.filter(status='interviewed').count()
    try:
        interviewed_pcnt = round(interviewed_number / matches_count * 100, 1)
    except ZeroDivisionError:
        interviewed_pcnt = 0

    rejected_number = matches.filter(status='rejected').count()
    try:
        rejected_pcnt = round(rejected_number / matches_count * 100, 1)
    except ZeroDivisionError:
        rejected_pcnt = 0

    

    offer_number = matches.filter(status='offergiven').count() 
    try:
        offer_pcnt = round(offer_number / matches_count * 100, 1)
    except ZeroDivisionError:
        offer_pcnt = 0
    
    total_contacted = (interviewed_number + shortlisted_number + offer_number)
    try:
        contacted_pcnt = round(total_contacted / matches_count * 100, 1)
    except ZeroDivisionError:
        contacted_pcnt = 0
    
    
    not_contacted = (matches_count - total_contacted)
    try:
       not_contacted_pcnt = round( not_contacted / matches_count * 100, 1)
    except ZeroDivisionError:
        not_contacted_pcnt = 0
    

    page = request.GET.get('page', 1)
    paginator = Paginator(matches, 10)
    try:
        match = paginator.page(page)
    except PageNotAnInteger:
        match = paginator.page(1)
    except EmptyPage:
        match =paginator.page(paginator.num_pages)

    context = {
        'match':match,
        'matches':matches,
        'matches_count':matches_count,

        'shortlisted_number':shortlisted_number,
        'shortlisted_pcnt':shortlisted_pcnt,

        'interviewed_number':interviewed_number,
        'interviewed_pcnt':interviewed_pcnt,

        'rejected_number':rejected_number,
        'rejected_pcnt':rejected_pcnt,

        'offer_number':offer_number,
        'offer_pcnt':offer_pcnt,

        'total_contacted':total_contacted,
        'contacted_pcnt':contacted_pcnt,

        'not_contacted':not_contacted,
        'not_contacted_pcnt':not_contacted_pcnt

    }
    return render(request,  'dash/ats.html', context)


def opps(request):
    opportunities = Opportunity.objects.filter(user=request.user).order_by('-id')
    opportunities_count = opportunities.count()
    expired = Opportunity.objects.filter(user=request.user, deadline__lt=datetime.now()).count()
    active = Opportunity.objects.filter(user=request.user, deadline__gte=datetime.now()).count()

    package = Package_Payment.objects.filter(user=request.user).last()

    try:
        percent_exp = round(expired / opportunities_count * 100,1)
    except ZeroDivisionError:
        percent_exp = 0
    try:
        percent_active = round(active / opportunities_count * 100,1)
    except ZeroDivisionError:
        percent_active = 0
    


    startup = get_object_or_404(Startup, user=request.user)

    page = request.GET.get('page', 1)
    paginator = Paginator(opportunities, 10)
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps =paginator.page(paginator.num_pages)
    

    if request.method == 'POST':
       
        form = oppForm(request.POST, request.FILES)
        print(request.POST)
        opp = Opportunity()
        if form.is_valid():
            opp.title = form.cleaned_data['title']
            opp.startup_name = startup
            opp.category = form.cleaned_data['category']
            opp.salary_range = form.cleaned_data['salary_range']
            opp.logo = form.cleaned_data['logo']
            opp.location = form.cleaned_data['location']
            opp.experience = form.cleaned_data['experience']
            opp.deadline = form.cleaned_data['deadline']
            opp.sector = form.cleaned_data['sector']
            opp.description = form.cleaned_data['description']
            opp.skills_required = form.cleaned_data['skills_required']
            opp.duties_and_responsibilities = form.cleaned_data['duties_and_responsibilities']
            opp.user = request.user 
            opp.save()
            package.posted_opportunity -= 1
            package.save()
            return redirect('opps')
        return redirect('dash')

    form = oppForm()
    context = {
        'opps':opps,
        'opportunities_count':opportunities_count,
        'form':form,
        'opportunities': opportunities,
        'is_expired':expired,
        'active':active,
        'percent_active':percent_active,
        'percent_exp':percent_exp,
        'package':package

    }
    return render(request,  'dash/opps.html', context)



def delete_opp(request,id):
    opp_id = Opportunity.objects.get(id=id)
    opp_id.delete()
    return redirect('opps')


def edit_opp(request, id):
    opp = Opportunity.objects.get(id=id)
    print(request.POST)
    if request.method == 'POST':
        opp.title = request.POST['title']
        opp.category = request.POST['category']
        opp.salary_range = request.POST['salary_range']
        if 'logo' in request.FILES:
            opp.logo = request.FILES['logo']
        opp.experience = request.POST['experience']
        opp.location = request.POST['location']
        opp.deadline = request.POST['deadline']
        opp.sector = request.POST['sector']
        opp.description = request.POST['description']
        opp.skills_required = request.POST['skills_required']
        opp.duties_and_responsibilities = request.POST['duties_and_responsibilities']
        opp.startup_name.id = request.POST['startup_name']
        opp.save()
        messages.success(request, 'Opportunity Updated Successful..')
        return redirect('opps')
    messages.error(request, 'Opportunity Update was not Successful..')
    return redirect('opps')



def matches(request):
    matches = Matches.objects.filter(startup=request.user.id).order_by('-id')[:5]
    matches_count = Matches.objects.filter(startup=request.user.id).count()

    opportunities = Opportunity.objects.filter(user=request.user)[:10]

    qs = request.GET.get('q')
    if qs:
        matches = matches.filter(
            Q(opportunity_title__icontains=qs)|
            Q(status__icontains=qs)| Q(user=request.user)).order_by('-id')
        

    page = request.GET.get('page', 1)
    paginator = Paginator(matches, 10)
    try:
        match = paginator.page(page)
    except PageNotAnInteger:
        match = paginator.page(1)
    except EmptyPage:
        match =paginator.page(paginator.num_pages)
    
    context ={
        'matches':matches,
        'matches_count':matches_count,
        'opportunities':opportunities,
        'match':match
    }
    return render(request, 'dash/matches.html',context)


def update_match(request, id):
    match = Matches.objects.get(id=id)
    if request.method == 'POST':
        match_status = request.POST['status']
        match.user_id = request.POST['user']
        match.status = request.POST['status']
        match.talent.id = request.POST['talent']
        match.startup.id = request.POST['startup']
        match.save()
        opportunity = request.POST['opportunity']
        match.opportunity.add(opportunity)
        if request.POST['via'] == 'gmeet':
            return redirect('https://meet.google.com')
        elif request.POST['via'] == 'zoom':
            return redirect('https://zoom.us')
        elif request.POST['via'] == 'mail':
            return redirect('https://mail.google.com')

        elif request.POST['via'] == 'shortlist':
            messages.success(request,f'{match.user.first_name} {match.user.last_name} has been Shortlisted')
            return redirect('matches')
        elif request.POST['via'] == 'reject':
            messages.success(request,f'{match.user.first_name} {match.user.last_name} has been Rejected')
            return redirect('matches')
        elif request.POST['via'] == 'offer':
            messages.success(request,f'{match.user.first_name} {match.user.last_name} has been Offered An Opportunity')
            return redirect('matches')

        elif match.status == match_status:
            messages.info(request,f'You have already started process or {match_status} {match.user.first_name} {match.user.last_name}')
            return redirect('matches')



def startup_profile(request):
    startup = get_object_or_404(Startup, user=request.user)

    rating = Startup_Rating.objects.filter(rating_for=startup)
    sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

    all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
    try:
       rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0

    if request.method == 'POST':
        print(request.POST)
        uform = userForm2(request.POST, instance=request.user)
        pform = profileForm(request.POST, request.FILES, instance=request.user.profile)
        sform = startupForm(request.POST, instance=startup)
        if uform.is_valid() and pform.is_valid()  and sform.is_valid():
            uform.save()
            pform.save()
            sform.save()
            messages.success(request, f"Succesful updated profile")
            return redirect('startup_profile')
    
    else:
        uform = userForm2(instance=request.user)
        pform = profileForm(instance=request.user.profile)
        sform = startupForm(instance=startup)
 

    context = {
        'data':startup,
        'rates':rates,
        'pform':pform,
        'uform':uform,
        'sform':sform,
    }
    return render(request, 'dash/profile.html', context)

def followers(request):
    startup = get_object_or_404(Startup, user=request.user)
    followers = startup.followers.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(followers, 20)
    try:
        follows = paginator.page(page)
    except PageNotAnInteger:
        follows = paginator.page(1)
    except EmptyPage:
        follows =paginator.page(paginator.num_pages)

    context ={
        'followers':followers,
        'follows':follows
    }
    return render(request, 'dash/followers.html', context)



def startup_messages(request):
    messages = Message.objects.all()
    threads = Thread.objects.all()
    context = {
        'messages':messages,
        'threads':threads
    }
    return render(request, 'dash/messages.html',context)
            
        
        


#==================================================================talent dash starts here======================================================================
@login_required(login_url='/auth')
def talent_dash(request):
    matches = Matches.objects.filter(user=request.user)

    page = request.GET.get('page', 1)
    paginator = Paginator(matches, 10)
    try:
        match = paginator.page(page)
    except PageNotAnInteger:
        match = paginator.page(1)
    except EmptyPage:
        match =paginator.page(paginator.num_pages)
    context = {
        'matches':matches,
        'match':match
    }
    return render(request, 'talent_dash/index.html', context)


def messages_view(request):
    messages = Message.objects.all()
    threads = Thread.objects.all()

    if request.method == 'POST':
        text = request.POST.get('text')
        thread = int( request.POST.get('thread'))
        response_data ={}
        message = Message(thread_id=thread, user=request.user, the_message=text)
        message.save()

        response_data['thread'] = message.thread_id
        return HttpResponse(
            json.dumps(response_data), 
            content_type = 'application/json'
        )

    # my_data = []
    # for dataz in messages:
    #     print(dataz.the_message)
    #     obj = {
    #         'user':{
    #             'id': dataz.user.id,
            
    #         },
    #         'message':dataz.the_message
    #     }
    #     my_data.append(obj)

       

    if request.is_ajax():
        message_ = Message.objects.all().values()
        list_of_dict = list(message_)
        # jsed =  serializers.serialize('json', message_)
        return JsonResponse(list_of_dict, safe=False)
      
    context = {
        'messages':messages,
        'threads':threads
    }
    return render(request, 'talent_dash/messages.html', context)

def talent_profile(request):
    talent = get_object_or_404(Talent, user=request.user)
    if request.method == 'POST':
        print(request.POST)
        uform = userForm(request.POST, instance=request.user)
        pform = profileForm(request.POST, request.FILES, instance=request.user.profile)
        tform = talentForm(request.POST, instance=talent)
        if uform.is_valid() and pform.is_valid() and tform.is_valid():
            uform.save()
            pform.save()
            tform.save()
            messages.success(request, f"Succesful updated profile")
            return redirect('profile')
    
    else:
        uform = userForm(instance=request.user)
        pform = profileForm(instance=request.user.profile)
        tform = talentForm(instance=talent)
    context = {
        'pform':pform,
        'uform':uform,
        'tform':tform
    }
    return render(request, 'talent_dash/profile.html', context)



def experience(request):
    talent = get_object_or_404(Talent, user=request.user)
    experience = Experience.objects.filter(talent=talent)
    exp_count = experience.count()
    exp = Experience()
    if request.method == 'POST':
        print(request.POST)
        form = addexpForm(request.POST or None)
        if form.is_valid():
            exp.talent = talent
            exp.company_name = form.cleaned_data['company_name']
            exp.start_date = form.cleaned_data['start_date']
            exp.finish_date = form.cleaned_data['finish_date']
            exp.still_working = form.cleaned_data['still_working']
            exp.position = form.cleaned_data['position']
            exp.details = form.cleaned_data['details']
            exp.save()
            messages.success(request, 'Submited sucessful!')
            return redirect('experience')

        messages.error(request, 'Submition Failed! make sure you fill all data correctly')
        return redirect('experience')
   

    context = {
        'experience':experience,
        'exp_count':exp_count
    }
    return render(request, 'talent_dash/experience.html',context)


def edit(request, id):
    talent = get_object_or_404(Talent, user=request.user)
    experience = Experience.objects.get(id=id)
    if request.method == 'POST':
        working = request.POST['still_working']
        fin_date =request.POST['finish_date']
        experience.talent_id = talent.id
        experience.company_name =request.POST['company_name']
        experience.start_date=request.POST['start_date']
        if working == 'Yes':
            experience.finish_date= None
        elif working == 'No' and fin_date == '':
            experience.finish_date= None
        else:
            experience.finish_date=request.POST['finish_date']
        experience.still_working=request.POST['still_working']
        experience.position=request.POST['position']
        experience.details=request.POST['details']
        experience.save()
        messages.success(request, 'Successful Update!')
        return redirect('experience')
    messages.error(request, 'form is not valid')
    return redirect('experience')



def delete_experience(request, id):
    experience = Experience.objects.get(id=id)
    experience.delete()
    messages.success(request, 'Deletion sucessful!')
    return redirect('experience')

    


def education(request):
    talent = get_object_or_404(Talent, user=request.user)
    education = Education.objects.filter(talent=talent)
    edu = Education()
    if request.method == 'POST':
        form = AddEduForm(request.POST or None)
        if form.is_valid():
            edu.talent = talent
            edu.speciality = form.cleaned_data['speciality']
            edu.start_date = form.cleaned_data['start_date']
            edu.end_date = form.cleaned_data['end_date']
            edu.school_name = form.cleaned_data['school_name']
            edu.details = form.cleaned_data['details']
            edu.save()
            messages.success(request, 'Submited sucessful!')
            return redirect('education')
        messages.error(request, 'Submition Failed! make sure you fill all data correctly')
        return redirect('education')

    context = {
        'education':education
    }
    return render(request, 'talent_dash/education.html', context)



def edit_education(request,id):
    edu = Education.objects.get(id=id)
    talent = get_object_or_404(Talent, user=request.user)
    if request.method == 'POST':
       edu.talent_id = talent.id
       edu.speciality = request.POST['speciality']
       edu.start_date = request.POST['start_date']
       edu.end_date = request.POST['end_date']
       edu.school_name = request.POST['school_name']
       edu.details = request.POST['details']
       edu.save()
       messages.success(request, 'Upadated successful!')
       return redirect('education')
    messages.error(request, 'Failed to update!!')
    return redirect('education')



def delete_education(request, id):
    education = Education.objects.get(id=id)
    education.delete()
    messages.success(request, 'Deletion sucessful!')
    return redirect('education')



def skills(request):
    talent = get_object_or_404(Talent, user=request.user)
    skills = Skill.objects.filter(talent=talent)

    if request.method == 'POST':
        skill = Skill()
        form = AddSkillForm(request.POST or None)
        if form.is_valid():
            skill.talent = talent
            skill.skill = form.cleaned_data['skill']
            skill.experience = form.cleaned_data['experience']
            skill.save()
            messages.success(request, 'Hoooray!! Skill added successful')
            return redirect('skills')
        messages.error(request, 'Opps!! Skill was not added')
        return redirect('skills')

    context = {
        'skills':skills
    }
    return render(request, 'talent_dash/skills.html', context)


def edit_skill(request,id):
    talent = get_object_or_404(Talent, user=request.user)
    skill = Skill.objects.get(id=id)
    if request.method == 'POST':
        skill.talent = talent
        skill.skill = request.POST.get('skill')
        skill.experience = request.POST.get('experience')
        skill.save()
        messages.success(request, 'Hoooray!! Skill added successful')
        return redirect('skills')
    messages.error(request, 'Opps!! Skill was not added')
    return redirect('skills')


def delete_skill(request,id):
    skill = Skill.objects.get(id=id)
    skill.delete()
    messages.success( request, f"{skill.skill} deleted successful!")
    return redirect('skills')




def job_alerts(request):
    opps = Opportunity.objects.all().order_by('-id')
    context = {
        'opps':opps
    }
    return render(request, 'talent_dash/alerts.html', context)





def bookmarks(request):
    marks  = Opportunity.objects.filter(marked=request.user)
    context = {
        'marks':marks
    }
    return render(request, 'talent_dash/bookmarks.html', context)


def reviews(request):
    talent = get_object_or_404(Talent, user=request.user)
    rating = Rating.objects.filter(rating_for_id=talent.id)

    sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

    all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
    try:
       rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0


    page = request.GET.get('page', 1)
    paginator = Paginator(rating, 8)
    try:
        ratings = paginator.page(page)
    except PageNotAnInteger:
        ratings = paginator.page(1)
    except EmptyPage:
        ratings =paginator.page(paginator.num_pages)

    context = {
        'rating':rating,
        'rates':rates,
        'ratings':ratings
    }
    return render(request, 'talent_dash/reviews.html', context)


#talents dash starts 


def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            if request.user.profile.user_type == 'talent':
                return redirect('talent_dash')
            elif request.user.profile.user_type == 'startup':
                return redirect('dash')
        
    else:
        form = PasswordChangeForm(request.user)
    context ={
            'form':form
        }
    return render(request, 'dash/passwordChange.html', context)

    