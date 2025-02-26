from rest_framework.viewsets import ModelViewSet

from configuration.models import Configuration, Review, Slider
from configuration.serializer import (ConfigurationSerializer,
                                      ReviewSerializer, SliderSerializer)


class SliderViewSet(ModelViewSet):
    queryset = Slider.objects.order_by('ordering')
    serializer_class = SliderSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.order_by('ordering')
    serializer_class = ReviewSerializer


class ConfigurationViewSet(ModelViewSet):
    queryset = Configuration.objects.order_by('-id').first()
    serializer_class = ConfigurationSerializer
