from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),

    path('register/', register, name='register'),

    path('login/', login_view, name='login'),

    path('logout/', LogoutView.as_view(next_page='profile'), name='logout'),

    path('profile/', profile, name='profile'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name='password_reset'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_sent.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path("chatbot/", chatbot, name="chatbot"),

    path('schedule-appointment/', schedule_appointment,
         name='schedule_appointment'),

    path('appointment/<int:appointment_id>/edit/',
         edit_appointment, name='edit_appointment'),

    path('appointment/<int:appointment_id>/delete/',
         delete_appointment, name='delete_appointment'),
]
