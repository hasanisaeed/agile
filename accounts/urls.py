from django.urls import path
from django.views.generic import TemplateView

from .views import DashboardView, signup_view, apply_attendance, LineChartJSONView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('attendance/<int:pk>', apply_attendance, name='attendance'),
    path('chart', TemplateView.as_view(template_name='performance.html'), name='line_chart'),
    path('chartJSON',  LineChartJSONView.as_view(), name='line_chart_json'),
]
