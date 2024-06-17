from django.urls import include, path
from .views import UserProfileDetailView, UserActiveDemandsView, create_demand_api, DemandDetailView, DemandDeleteView

urlpatterns = [
        path('user/<int:pk>/', UserProfileDetailView.as_view(), name='user_detail'),
        path('user/<str:telegram_id>/demands/', UserActiveDemandsView.as_view(), name='user-active-demands'),
        path('api/create_demand/', create_demand_api, name='create_demand_api'),
        path('api/demand/<int:pk>/', DemandDeleteView.as_view(), name='demand_delete'),
]