
from django.contrib import admin 
from django.urls import path, include 
from accounts.views import upload_location
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('', home), 
    path('api/location/', upload_location),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    
]


