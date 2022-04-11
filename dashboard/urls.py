from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    #startup links
    path('dash', views.dash, name='dash'),
    path('ats', views.ats, name='ats'),
    path('packages', views.packages, name='packs'),
    path('zoom', views.zoom,name='zoom'),
    path('callback', views.payment_response, name='payment_response'),


    path('matches', views.matches, name='matches'),
    path('update-match/<int:id>', views.update_match, name="update_match"),

    path('startup-profile', views.startup_profile, name='startup_profile'),
    path('followers', views.followers, name='followers'),
    path('my-messages', views.startup_messages,name='startup_messages'),


    path('my-opportunities', views.opps, name='opps'),
    path('delete/<int:id>', views.delete_opp, name='delete'),
    path('edit-opportunity/<int:id>', views.edit_opp, name='edit_opportunity'),
    #endstartup links


    #talent links
    path('talent-dash', views.talent_dash, name='talent_dash' ),
    path('message', views.messages_view, name='user_message' ),
    path('profile', views.talent_profile, name='profile' ),
   

    path('experience', views.experience, name='experience' ),
    path('delete-experience/<int:id>', views.delete_experience, name='delete_experience' ),
    path('edit-experience/<int:id>', views.edit, name='edit_experience' ),


    path('education', views.education, name='education' ),
    path('edit-education/<int:id>', views.edit_education, name="edit_education"),
    path('delete-education/<int:id>', views.delete_education, name='delete_education' ),

    path('skills', views.skills, name='skills'),
    path('edit-skill/<int:id>', views.edit_skill, name='edit_skill'),
    path('delete-skill/<int:id>', views.delete_skill, name='delete_skill'),

    path('job-alerts', views.job_alerts, name="alerts"),

    path('bookmarks',views.bookmarks, name='bookmarks'),

    path('reviews', views.reviews,name='reviews'),

    path('change-password', views.changePassword,name='pwd_change'),
]