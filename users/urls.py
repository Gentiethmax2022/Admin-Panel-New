from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('transactions/', views.view_all_transactions, name='view_all_transactions'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('register/', views.register_view, name='register'),
    path('admin_user/', views.admin_view, name='admin'),
]



