from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

from authapp.forms import CustomUserCreateForm
from cloudapp.models import CustomUser
from cloudapp.views import logout_view

app_name = 'custom_auth'

urlpatterns = [
    path('sign-up/', CreateView.as_view(template_name='authapp/sign-up.html',
                                        success_url=reverse_lazy('custom_auth:login'),
                                        form_class=CustomUserCreateForm,
                                        model=CustomUser), name='registration'),
    path('sign-in/', LoginView.as_view(template_name='authapp/sign-in.html'), name='login'),
    path('logout/', logout_view, name='logout')
]