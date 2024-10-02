from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # Include blog app URLs
    path('users/', include('users.urls')),  # Include users app URLs
    path('', include('blog.urls')),  # Redirect the homepage to the blog post list
]