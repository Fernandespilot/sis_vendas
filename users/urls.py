from django.urls import path
from .views import CustomLoginView, password_change, perfil, logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_change/', password_change, name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', logout, name='logout'),
]
