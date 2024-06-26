from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from profiles.models import Profile, Relationship
from profiles.forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from posts.forms import CommentModelForm
# Create your views here.

def home_view(request):
    return render(request, 'main/home.html', {'hello': 'hello'})


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            
    ctx = {'profile': profile, 'form': form, 'confirm': confirm}
    return render(request, 'profiles/myprofile.html', ctx)


@login_required
def get_friend_list(request):
    my_profile = Profile.objects.get(user=request.user)
    friends_list = []
    users = Profile.objects.get(user=request.user).get_friends()
    for user in users:
        profile = Profile.objects.get(user=user)
        friends_list.append(profile)
    total_friends = len(friends_list)
    return render(request, 'profiles/friends_list.html', {'friends': friends_list, 'my_profile': my_profile, 'total_friends': total_friends})


@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    invites = Relationship.objects.invitations_received(profile)
    invite_senders = list(map(lambda x: x.sender, invites))
    is_empty = False
    if len(invite_senders) == 0:
        is_empty = True
    return render(request, 'profiles/my_invites.html', {'invites': invite_senders, 'is_empty':is_empty})


@login_required
def invite_profiles_list_view(request):
    profile = Profile.objects.get(user=request.user)
    profiles = Profile.objects.get_all_profiles_to_invite(request.user)
    rel = Relationship.objects.filter(sender=profile)
    receivers = []
    for relation in rel:
        receivers.append(relation.receiver)
    return render(request, 'profiles/to_invite_list.html', {'profiles': profiles, 'receivers': receivers})


def requested_profiles_list(request):
    profile = Profile.objects.get(user=request.user)
    # profiles = Profile.objects.get_all_profiles_to_invite(request.user)
    rel = Relationship.objects.filter(sender=profile)
    receivers = []
    for relation in rel:
        receivers.append(relation.receiver)
    return render(request, 'profiles/requested_profiles_list.html', {'receivers': receivers})
        

@login_required
def cancel_request(request):
    if request.method == 'POST':
        sender = Profile.objects.get(user=request.user)
        receiver_id = request.POST.get('profile_id')
        receiver = Profile.objects.get(id=receiver_id)
        print(sender)
        print(receiver)
        relationship = Relationship.objects.get(sender=sender, receiver=receiver)
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:invite-profiles-view')


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relationship.status == 'sent':
            relationship.status = 'accepted'
            relationship.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-invites')


@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-invites')


class ProfileDetailView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        user_profile = Profile.objects.get(user=self.request.user)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_r = Relationship.objects.filter(sender=profile)

        sender_list = []
        receiver_list = []
        for item in rel_s:
            sender_list.append(item.sender.user)

        for item in rel_r:
            receiver_list.append(item.receiver.user)

        context['c_form'] = CommentModelForm()
        context['sender_list'] = sender_list
        context['receiver_list'] = receiver_list
        context['user_profile'] = user_profile
        context['posts'] = self.get_object().get_all_posts()
        context['len_posts'] = True if len(self.get_object().get_all_posts()) > 0 else False
        
        return context


class ProfileListView(ListView, LoginRequiredMixin):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        search_input = self.request.GET.get('search-area')
        if search_input:
            qs = Profile.objects.filter(user__username__icontains=search_input)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_r = Relationship.objects.filter(sender=profile)

        sender_list = []
        receiver_list = []
        for item in rel_s:
            sender_list.append(item.sender.user)

        for item in rel_r:
            receiver_list.append(item.receiver.user)

        context['sender_list'] = sender_list
        context['receiver_list'] = receiver_list
        context['user_profile'] = profile
        print('sneder', sender_list)
        print('receiver', receiver_list)
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context
    

@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)
        relationship = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')


@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')
