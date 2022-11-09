from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from auth.forms import SignupForm

# Create your views here.

class Login(LoginView):
    template_name = 'auth/login.html'

class Logout(LogoutView):
    pass

class Signup(View):

    def get(self, request):
        context = {
            'form': SignupForm()
        }
        return render(request, 'auth/signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        context = {
            'form': form 
        }
        return render(request, 'auth/signup.html', context)