from django.urls import path
from . import views

from django.urls import path
# from .views import user_login, user_signup, user_logout
from .views import property_list, post_property, index, login_view, signup_view, logout_view


urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('post-property/', views.post_property, name='post_property'),

    # Authentication URLs
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]

