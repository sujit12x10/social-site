from profiles.models import Profile, Relationship


def invitation_receiced_no(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        count = Relationship.objects.invitations_received(profile).count()
        return {'invites_count': count}
    return {}

def requested_profiles_no(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # profiles = Profile.objects.get_all_profiles_to_invite(request.user)
        rel = Relationship.objects.filter(sender=profile)
        receivers = []
        for relation in rel:
            receivers.append(relation.receiver)
        receivers_count = len(receivers)
        return {'receivers_count': receivers_count}
    return {}