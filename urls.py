from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('predict/', views.predict_view, name='predict'),
    path('result/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
]
