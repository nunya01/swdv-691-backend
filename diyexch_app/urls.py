from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.nologin_home),
    path('search_by_name/<str:name>', views.search_by_name),
    path('tool_home/<int:t_id>/', views.tool_home),
    path('create_tool/', views.create_tool),
    path('delete_tool/<int:t_id>/', views.delete_tool),
    path('contact/<int:id>', views.contact),
    path('search/', views.search, name="search"),
    path('borrow_tool/<int:t_id>/', views.borrow_tool),
    path('rate_user/<int:id>', views.rate_user), # stretch
    path('account_home/', views.account_home, name="home"),
    path('test_function/', views.test_function),
    path('profile/', views.profile),
    path('first_login/', views.first_login),
]