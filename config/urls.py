from django.contrib import admin
from django.urls import path, include

from accounts.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', DashboardView.as_view(), name='home'),
]
