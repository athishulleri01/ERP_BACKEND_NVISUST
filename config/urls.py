from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    # --------------------------------------------------------------------------------------------------------------
    # -----------------------------------Admin Pannel---------------------------------------------------------------
    path('admin/', admin.site.urls),
    
    # --------------------------------------------------------------------------------------------------------------
    # --------------------------------------Token Refreshing---------------------------------------------------------
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/auth/', include('authentication.urls')),
    
]