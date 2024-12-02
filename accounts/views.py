from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from .models import CustomUser, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm

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

# class ProfileEditView(UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'accounts/edit_profile.html'
#     context_object_name = 'profile'
#     # You can specify the success URL or let it default to the same page

#     def get_success_url(self):
#         # After saving, redirect to the profile page
#         return reverse_lazy('profile', kwargs={'pk': self.object.pk})

class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "registration/confirm_delete.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user