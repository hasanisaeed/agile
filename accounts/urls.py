from django.urls import path

from .views import DashboardView, signup_view

# from .views import SignUpView, DashboardView


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
