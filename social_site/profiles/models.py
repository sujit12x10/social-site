from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
# Create your models here.

class ProfileManager(models.Manager):

    def get_all_profiles(self, me):
        qs = Profile.objects.all().exclude(user=me)
        return qs

    def get_all_profiles_to_invite(self, sender):
        profile = Profile.objects.get(user=sender)
        profile_friends = profile.friends.all()
        profiles = Profile.objects.all().exclude(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        rel_exits = set([])
        for rel in qs:
            # if rel.status == 'accepted':
            #     accepted.add(rel.receiver)
            #     accepted.add(rel.sender)
            rel_exits.add(rel.sender)
            rel_exits.add(rel.receiver)

        available = [profile for profile in profiles if profile not in rel_exits and profile not in profile_friends]
        return available
    

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...', blank=True, max_length=60)
    email = models.EmailField(blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    friends = models.ManyToManyField(User, blank=True, related_name='friends',)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self, *args, **kwargs):
        return reverse('profiles:profile-detail-view', kwargs={'slug': self.slug})

    def get_total_posts(self):
        return self.posts.all().count()
    
    def get_all_posts(self):
        return self.posts.all()
    
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1
        return total_likes
    
    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name
        
    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.all().exclude(user=self.user).filter(slug=to_slug)
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.all().exclude(user=self.user).filter(slug=to_slug)
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    
STATUS_CHOICES = (
    ('sent', 'sent'),
    ('accepted', 'accepted')
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status = 'sent')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
