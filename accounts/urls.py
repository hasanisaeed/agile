from django.urls import path

from utils.dataset_model import ChartModelView
from .views import DashboardView, apply_attendance

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('attendance/<int:pk>', apply_attendance, name='attendance'),
    path('chart', ChartModelView.as_view(), name='line_chart'),
]
