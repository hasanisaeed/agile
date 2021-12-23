from django.urls import path

from utils.dataset_model import ChartModelView
from .views import DashboardView, signup_view, apply_attendance

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('attendance/<int:pk>', apply_attendance, name='attendance'),
    path('chart', ChartModelView.as_view(), name='line_chart'),
]
