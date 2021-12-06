from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.account_home, name="home"),
    path('tool_home/<int:t_id>/', views.tool_home),
    path('create_tool/', views.create_tool),
    path('delete_tool/<int:t_id>/', views.delete_tool),
    path('contact/<int:id>', views.contact),
    path('search/', views.search, name="search"),
    path('borrow_tool/<int:t_id>/', views.borrow_tool),
    path('rate_user/<int:id>', views.rate_user), # stretch
    path('account_home/', views.account_home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name="about"),
]