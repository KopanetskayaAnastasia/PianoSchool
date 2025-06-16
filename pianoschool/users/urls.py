from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import LoginUser, RegisterUser, logout_user, personalisation, \
    CustomPasswordChangeDoneView, delete_profile

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('personalisation/', personalisation, name='personalisation'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('profile/delete/', delete_profile, name='delete_profile'),
]

