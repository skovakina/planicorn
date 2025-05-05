from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Board model
class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    location = models.CharField(max_length=255, blank=True) 
    start_date = models.DateField(null=True, blank=True)    
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.name

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tag')
    color = models.CharField(max_length=7, default='#CCCCCC')

    def __str__(self):
        return self.name

# Event model
class Event(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    @property
    def duration_in_minutes(self):
        return (self.end_time - self.start_time).total_seconds() / 60

    

# Profile model (extending User)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Signal to automatically create/update profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
