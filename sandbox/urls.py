"""sandbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

handler404 = 'home.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('', include('home.urls')),
    path('', include('talents.urls')),
    path('', include('startups.urls')),
    path('', include('opportunity.urls')),
    path('', include('userauth.urls')),
    path('', include('dashboard.urls')),

    #social logins url
    # path('oauth/', include('social_django.urls', namespace='social')), 


    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html'),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'),name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name="password_reset_complete"),
]



if settings.DEBUG:
    urlpatterns += static(
         settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

