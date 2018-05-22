from django.shortcuts import render, redirect
from django.views.generic import CreateView,FormView
from .forms import RegisterForm, LoginForm
from django.utils.http import is_safe_url
from ct_blog.mixins import NextUrlMixin, RequestFormAttachMixin

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)
