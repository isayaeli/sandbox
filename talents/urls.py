from django.urls import path
from . import views

urlpatterns = [
    path('talents', views.talents, name='talents' ),
    path('talent/<str:slug>', views.talent_details, name='talent_details'),
    path('rate/<str:slug>/', views.rate, name='rate')
]