from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),  # custom admin app
    path('api/', include('api.urls')),     # API endpoints
]

# Serve media files in development only
