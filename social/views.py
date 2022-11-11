from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from social import models, forms

# Create your views here.

# Home screen to show posts of friends
class Wall(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'social/wall.html'
    login_url = 'auth/login'
    
    def get_queryset(self):
        friendsIds = [friend.person2.id for friend in models.Friend.objects.filter(person1 = self.request.user)]
        friendsIds += [friend.person1.id for friend in models.Friend.objects.filter(person2 = self.request.user)]

        return models.Post.objects.filter(user__in = friendsIds).order_by('-created_at')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = forms.CommentForm
        return data

# Profile screen to show my posts.
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

# Create post
class PostCreate(View):
    def post(self, request):
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

        return redirect("/profile")

# Delete Post
class PostDelete(View):
    def get(self, request, pk):
        models.Post.objects.get(pk=pk).delete()
        return redirect("/profile")

# Like Post
class PostLike(View):
    def get(self, request, pk):
        # user and post in like: do nothing.
        try:
            models.Like.objects.get(
                user = request.user,
                post = models.Post.objects.get(pk=pk)
            ).delete()
        except:
            models.Like.objects.create(
                user = request.user,
                post = models.Post.objects.get(pk=pk)
            )
        return redirect("/")

class PostComment(View):
    def post(self, request, pk):
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = models.Post.objects.get(pk=pk)
            comment.save()
        return redirect("/")

# New Friends
class Users(ListView):
    context_object_name = 'users'
    template_name = 'social/users.html'

    def get_queryset(self):

        return models.User.objects.all()

    def get_context_data(self, *args, **kwargs):
        # My Friends
        excludeIds = [friend.person2.id for friend in models.Friend.objects.filter(person1 = self.request.user)]
        excludeIds += [friend.person1.id for friend in models.Friend.objects.filter(person2 = self.request.user)]
        friends = models.User.objects.filter(id__in=excludeIds)

        # Sent Requests
        sentReqIds = [friend.requestee.id for friend in models.FriendRequest.objects.filter(requester=self.request.user)]
        sentReqs = models.User.objects.filter(id__in=sentReqIds)
        excludeIds += sentReqIds

        # Recieved Requests
        recievedReqIds = [friend.requester.id for friend in models.FriendRequest.objects.filter(requestee=self.request.user)]
        recievedReqs = models.User.objects.filter(id__in=recievedReqIds)
        excludeIds += recievedReqIds

        # Remove current user
        excludeIds += [self.request.user.id]

        # New Friends
        nonFriends = models.User.objects.all().exclude(id__in=excludeIds)

        context = {
            'friends': friends,
            'nonfriends': nonFriends,
            'sentreqs': sentReqs,
            'recievedreqs': recievedReqs,
        }

        return context 

# Add Friend
class AddFriend(View):
    
    def get(self, request, pk):
        models.FriendRequest.objects.create(requester=request.user, requestee=models.User.objects.get(pk=pk))
        return redirect("/users")

# Remove Friend
class RemoveFriend(View):
    
    def get(self, request, pk):
        try:
            models.Friend.objects.get(person1=request.user, person2=models.User.objects.get(pk=pk)).delete()
        except:
            models.Friend.objects.get(person2=request.user, person1=models.User.objects.get(pk=pk)).delete()
        return redirect("/users")

class FriendRequestCancel(View):
    def get(self, request, pk):
        models.FriendRequest.objects.filter(requester=request.user, requestee=models.User.objects.get(pk=pk)).delete()
        return redirect("/users")

class FriendRequestAccept(View):
    def get(self, request, pk):
        models.FriendRequest.objects.filter(requestee=request.user, requester=models.User.objects.get(pk=pk)).delete()
        models.Friend.objects.create(person1=request.user, person2=models.User.objects.get(pk=pk))
        return redirect("/users")
