from rest_framework.routers import DefaultRouter
from django.urls import path
from configuration.api import (ConfigurationRetrieveView, ReviewViewSet,
                               SliderViewSet)

router = DefaultRouter()
router.register(r'sliders', SliderViewSet, basename="sliders")
router.register(r'reviews', ReviewViewSet, basename="reviews")


urlpatterns = router.urls
urlpatterns = +[
    path('configuration/', ConfigurationRetrieveView.as_view(), name='configuration-detail'),
]
