from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.nologin_home),
    path('register/', views.register),
    path('users/<int:id>', views.user),
    path('tools/<int:id>', views.tool),
    path('search_by_name/<str:name>', views.search_by_name),
    path('create_user/', views.create_user),
    path('tool_form/', views.tool_form),
    path('preview_tool/<int:id>', views.preview_tool),
    path('create_tool/', views.create_tool),
    path('contact/<int:id>', views.contact),
    path('search/', views.search),
    path('borrow_tool/', views.borrow_tool),
    path('rate_user/<int:id>', views.rate_user) # stretch
]