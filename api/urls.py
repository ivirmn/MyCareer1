from django.urls import include, path
from .views import UserProfileDetailView

urlpatterns = [
        path('user/<int:pk>/', UserProfileDetailView.as_view(), name='user_detail'),
]