import uuid
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import AppUserManager

# Create your models here.

class User(AbstractUser):
    # fields removed from base user model
    first_name = None
    last_name = None

    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField('full name', max_length=255)
    date_of_birth = models.DateField(_('date of birth'),null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    objects = AppUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def is_member_of(self, group):
        return self.groups.filter(name=group).exists()

    def is_member_of_only(self, groups):
        pass

    def is_member_of_either(self, groups):
        pass

    def is_in_multiple_groups(self, groups):
        return self.groups.filter(name__in=groups).exists()


class OnlineStatus(models.Model):
    STATUS_CHOICE = (
        ('Online', 'Online'),
        ('Offline', 'Offline')
    )
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='online')
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, blank=True)

