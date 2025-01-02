from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
    path('getProfile/', views.GetProfileView.as_view(), name='get_profile'),
]
