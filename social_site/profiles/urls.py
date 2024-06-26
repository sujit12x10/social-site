from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('myprofile/', views.my_profile_view, name='my-profile-view'),
    path('my-friends/', views.get_friend_list, name='my-friends-list-view'),
    path('my-invites/', views.invites_received_view, name='my-invites'),
    path('requested-profiles-list/', views.requested_profiles_list, name='requested-profiles-list-view'),

    path('send-invitation/', views.send_invitation, name='send-invitation'),
    path('accept-invitation/', views.accept_invitation, name='accept-invitation'),
    path('reject-invitation/', views.reject_invitation, name='reject-invitation'),

    path('to-invite/', views.invite_profiles_list_view, name='invite-profiles-view'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),

    path('cancel-request/', views.cancel_request, name='cancel-request-view'),
    
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),

]


