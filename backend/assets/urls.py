from rest_framework.routers import DefaultRouter
from .views import AssetInstanceViewSet

router = DefaultRouter()
router.register(r'instances', AssetInstanceViewSet, basename='instances')

urlpatterns = router.urls