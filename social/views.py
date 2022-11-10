from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from social import models, forms

# Create your views here.

class Wall(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'social/wall.html'
    login_url = 'auth/login'
    
    def get_queryset(self):
        friendsIds = [friend.person2.id for friend in models.Friend.objects.filter(person1 = self.request.user)]
        friendsIds += [friend.person1.id for friend in models.Friend.objects.filter(person2 = self.request.user)]

        return models.Post.objects.filter(user__in = friendsIds).order_by('-created_at')

class Profile(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'social/profile.html'
    login_url = 'auth/login'

    def get_queryset(self):
        return models.Post.objects.filter(user = self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['post_form'] = forms.PostForm
        return data

class Post(View):
    def post(self, request):
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

        return redirect("/profile")

class Users(ListView):
    context_object_name = 'users'
    template_name = 'social/users.html'

    def get_queryset(self):
        excludeIds = [friend.person2.id for friend in models.Friend.objects.filter(person1 = self.request.user)]
        excludeIds += [friend.person1.id for friend in models.Friend.objects.filter(person2 = self.request.user)]
        excludeIds += [self.request.user.id]

        return models.User.objects.all().exclude(id__in=excludeIds)

class AddFriend(View):
    
    def get(self, request, pk):
        models.Friend.objects.create(person1=request.user, person2=models.User.objects.get(pk=pk))
        return redirect("/")
