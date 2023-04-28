from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'

urlpatterns = [
    path('', views.home_view, name='home'),  #type: ignore 
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('risk_assessment/', views.risk_assessment, name='risk_assessment'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('register/', views.register_view, name='register'),
    path('search_transactions/', views.search_transactions, name='search_transactions'),
    path('reports/', views.reports, name='reports'),
    path('new_transaction/', views.new_transaction, name='new_transaction'),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





