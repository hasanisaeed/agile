from django.urls import path

from .views import DashboardView, signup_view, apply_attendance, line_chart, line_chart_json

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('attendance/<int:pk>', apply_attendance, name='attendance'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]
