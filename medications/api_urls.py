from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, PharmacyMedicationViewSet

router = DefaultRouter()
router.register('drugs', MedicationViewSet)
router.register('inventory', PharmacyMedicationViewSet, basename='pharmacy-medication')

urlpatterns = router.urls