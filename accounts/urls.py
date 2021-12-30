from django.urls import path

from accounts.views.chart import ChartModelView
from accounts.views.dashboard import DashboardView, apply_attendance

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('attendance/<int:pk>', apply_attendance, name='attendance'),
    path('chart', ChartModelView.as_view(), name='line_chart'),
]
