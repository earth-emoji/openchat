from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView

from accounts.forms import UserSignUpForm
from accounts.models import UserProfile
from users.models import User

# Create your views here.
def home(request, template_name='accounts/home.html'):
    if request.user.is_authenticated:
        return redirect('profile:index', request.user.profile.slug)
    return render(request, template_name)

class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'User'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile:index', request.user.profile.slug)


def signup_success(request, template_name='accounts/success.html'):
    return render(request, template_name)

def logout_view(request):
    logout(request)
    return redirect('home')