import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy

class UserProfileManager(models.Manager):
    use_for_related_fields = True

# Create your models here. 
class UserProfile(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    contacts    = models.ManyToManyField('self', related_name='contacts', blank=True)    

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username
