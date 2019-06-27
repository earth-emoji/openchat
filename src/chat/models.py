import uuid
from django.db import models
from django.utils.text import slugify

from accounts.models import UserProfile


class Room(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="rooms", blank=True)
    name = models.CharField(max_length=60, unique=True, blank=True)
    members = models.ManyToManyField(UserProfile, related_name="room_memberships", blank=True)
    black_list = models.ManyToManyField(UserProfile, related_name="rooms_forbidden", blank=True)
    is_active = models.BooleanField(default=True)

    url = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Room, self).save(*args, **kwargs) 

    def __str__(self):
        return self.name

class Message(models.Model):
    slug        = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    room        = models.ForeignKey(Room, blank=True, on_delete=models.CASCADE, related_name='messages')
    sender      = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages')
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class RoomRequest(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    # user requesting
    sender = models.ForeignKey(UserProfile, related_name='room_requests_sent', on_delete=models.CASCADE)
    
    # user requested
    receiver = models.ForeignKey(UserProfile, related_name='room_requests_received' , on_delete=models.CASCADE)
    
    # status
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)