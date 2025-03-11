from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('post-property/', views.post_property, name='post_property'),
]
