from django.urls import path
from .views import SignUpView, ProfileEditView, ProfilePageView, DeleteAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit_profile/<int:pk>/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<int:pk>/', ProfilePageView.as_view(), name='view_profile'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
]