from django.urls import path
from rest_framework.routers import DefaultRouter

from configuration.api import (ConfigurationRetrieveView, ReviewViewSet, ContactUsViewSet,
                               SliderViewSet)

router = DefaultRouter()
router.register(r'sliders', SliderViewSet, basename="sliders")
router.register(r'reviews', ReviewViewSet, basename="reviews")
router.register(r'contact-us', ContactUsViewSet, basename="contactus")

urlpatterns = router.urls

urlpatterns += [
    path('configuration/', ConfigurationRetrieveView.as_view(), name='configuration-detail'),
]
