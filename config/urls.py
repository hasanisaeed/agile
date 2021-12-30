from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views.dashboard import DashboardView

urlpatterns = \
    [path('admin/', admin.site.urls),
     path('accounts/', include('accounts.urls')),
     path('accounts/', include('django.contrib.auth.urls')),
     path('', DashboardView.as_view(), name='home'),
     ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
