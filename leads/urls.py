from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard-enaile-exclusivo/', views.dashboard, name='dashboard'),
]