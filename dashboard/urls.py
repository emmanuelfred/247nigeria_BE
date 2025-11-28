from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_login, name='dashboard_login'),
   
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
        path('jobs/pending/', views.pending_jobs, name='pending_jobs'),
    path('properties/pending/', views.pending_properties, name='pending_properties'),
    path('messages/', views.dashboard_messages, name='messages'),
    path('users/', views.users, name='users'),
    path('teams/', views.teams, name='teams'),
    path('advertisement/', views.advertisement, name='advertisement'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.dashboard_settings, name='settings'),
    path("team/add/", views.add_team_admin, name="add_team_admin"),
    path('team/', views.team_list, name='team_list'),
    path('update_user/', views.update_user_settings, name='update_user_settings'),
    path('update_password/', views.update_password, name='update_password'),
    path('delete-user/<int:admin_id>/', views.delete_admin, name='delete_user'),
    path('delete-admin/<int:admin_id>/', views.delete_team_admin, name='delete_admin'),
    path('verify_user/<int:admin_id>/', views.verify_user, name='verify_user'),
    path("login/", views.admin_login, name="admin_login"),
    path("update_profile_picture/", views.update_profile_picture, name="update_profile_picture"),
   
    path("logout/", views.admin_logout, name="admin_logout"),
]
