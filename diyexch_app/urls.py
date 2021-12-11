from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.account_home, name="home"),
    path('tool_home/<int:t_id>/', views.tool_home),
    path('create_tool/', views.create_tool, name="share"),
    path('delete_tool/<int:t_id>/', views.delete_tool),
    path('search/', views.search, name="search"),
    path('borrow_tool/<int:t_id>/', views.borrow_tool),
    path('rate_user/<int:id>', views.rate_user), # stretch
    path('account_home/', views.account_home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('req_confirm/<int:b_id>/', views.req_confirm),
    path('cancel_borrow/<int:b_id>/', views.cancel_borrow),
    path('approve_borrow/<int:b_id>/', views.approve_borrow),
    path('return_tool/<int:b_id>/', views.return_tool),
    path('update_tool/<int:t_id>/', views.update_tool),
]