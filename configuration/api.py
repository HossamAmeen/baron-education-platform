from rest_framework.generics import RetrieveAPIView
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


class ConfigurationRetrieveView(RetrieveAPIView):
    serializer_class = ConfigurationSerializer

    def get_object(self):
        return Configuration.objects.order_by('-id').first()
