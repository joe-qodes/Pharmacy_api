from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML views
    path('', include('accounts.urls')),
    path('', include('pharmacies.urls')),
    path('', include('orders.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # REST API
    path('api/accounts/', include('accounts.api_urls')),
    path('api/pharmacies/', include('pharmacies.api_urls')),
    path('api/medications/', include('medications.api_urls')),
    path('api/prescriptions/', include('prescriptions.api_urls')),
    path('api/orders/', include('orders.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)