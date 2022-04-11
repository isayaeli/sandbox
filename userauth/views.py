import email
from django.shortcuts import render, redirect
from .forms import NewUserForm, profileForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.models import User
from startups.models import Startup
from talents.models import Talent

def auth_view(request):
    return render(request, 'auth/auth.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request,'User with this email already exists you may need to use a different email!!')
                return redirect('auth')
            else:
                user = form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                messages.success(request, "Registration successful.")
            
            if request.user.profile.user_type == 'not_set':
                return redirect("user_type")
           
        # messages.error(request, "form is not valid.")
        # return redirect('auth')
    # else:
    #     form = NewUserForm()
    # context = {
    #     'form':form
    # }
    return render(request, 'auth/auth.html')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                if request.user.profile.user_type == 'not_set':
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("user_type")
                elif request.user.profile.user_type == 'startup':
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('dash')
                elif request.user.profile.user_type == 'talent':
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('talent_dash')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('auth')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('auth')
    # form = AuthenticationForm()
    return render(request, 'auth/auth.html')



def user_type(request):
    if request.method == 'POST':
        form = profileForm(request.POST, instance=request.user.profile)
        print(request.POST)
        if form.is_valid():
            form.save()
            if request.user.profile.user_type == 'startup':
                starup  = Startup.objects.create(user=request.user)
                starup.save()

            elif request.user.profile.user_type == 'talent':
                talent  = Talent.objects.create(user=request.user)
                talent.save()

            if request.user.profile.user_type == 'talent':      
                return redirect('talent_dash')
            elif request.user.profile.user_type == 'startup':
                return redirect('dash')
            else:
                return redirect('user_type')

        return redirect('user_type')
    form = profileForm(instance=request.user.profile)
    return render(request, 'auth/user_type.html',{'form':form})


def logout_request(request):
    logout(request)
    messages.info(request,f"Logged out successful")
    return redirect('home')