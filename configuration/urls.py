from rest_framework.routers import DefaultRouter

from configuration.api import (ConfigurationRetrieveView, ReviewViewSet,
                               SliderViewSet)

router = DefaultRouter()
router.register(r'sliders', SliderViewSet, basename="sliders")
router.register(r'reviews', ReviewViewSet, basename="reviews")
router.register(r'configuration',
                ConfigurationRetrieveView.as_view(), basename='configuration')

urlpatterns = router.urls
