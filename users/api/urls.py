from django.urls import path
from users.api.views import (
    registration_view,
    update_account_view,
    account_view

)
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'account'

urlpatterns = [
    path('login', obtain_auth_token, name='login'),
    path('properties', account_view, name='properties'),
    path('properties/update', update_account_view, name='update'),
    path('register', registration_view, name='register'),

]