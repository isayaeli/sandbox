from django.urls import  path
from . import views
urlpatterns = [
   path('login', views.login_request,  name='login' ),
   path("register", views.register_request, name='register'),
   path('auth', views.auth_view,  name='auth' ),
   # path("login", views.login_request, name="login"),
   path('user-type', views.user_type, name='user_type'),
   path("logout", views.logout_request, name="logout"),
]