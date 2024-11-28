from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from .models import CustomUser, Profile

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = CustomUser.objects.get(username=username)
            customer_group = form.cleaned_data.get('group')
            customer_group.user_set.add(signup_user)

            return redirect('login')
        else:
            return render(
                request, 
                self.template_name, 
                {'form' : form }
            )
        
class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')
    fields = [
        'date_of_birth',
        'fav_artist',
        'fav_album',
        'fav_genre',
    ]

class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'