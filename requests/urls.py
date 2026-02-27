from rest_framework.routers import DefaultRouter
from .views import RequestViewSet

router = DefaultRouter()
router.register('', RequestViewSet)

urlpatterns = router.urls