from django.urls import path
from . import views

urlpatterns = [
    # --------------------------------------------------------------------------------------------------------------
    # -----------------------------------Authentication-------------------------------------------------------------
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # -------------------------------------------------------------------------------------------------------------
    # -----------------------------------User actions---------------------------------------------------------------
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]