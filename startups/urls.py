from unicodedata import name
from django.urls import path
from .import views
urlpatterns = [
    path('startups',views.startups, name='startups'),
    path('startup/<int:id>',views.startup_details, name='startup_details'),
    path('follow', views.follow , name='follow'),
    path('rate-startup/<int:id>/', views.rate, name='rate_startup')
]