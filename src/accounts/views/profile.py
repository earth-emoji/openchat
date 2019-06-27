from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from users.decorators import group_required
from users.models import User
from accounts.models import UserProfile

@login_required
def user_profile(request, slug, template_name='accounts/profile/index.html'):
    profile = get_object_or_404(UserProfile, slug=slug, user=request.user)
    data = {}
    data['profile'] = profile
    return render(request, template_name, data)

