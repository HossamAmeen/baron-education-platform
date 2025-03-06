from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from configuration.models import Configuration, ContactUs, Review, Slider
from configuration.serializer import (ConfigurationSerializer,
                                      ContactUsSerializer, ReviewSerializer,
                                      SliderSerializer)


class SliderViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Slider.objects.order_by('ordering')
    serializer_class = SliderSerializer


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Review.objects.order_by('ordering')
    serializer_class = ReviewSerializer


class ContactUsViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = ContactUs.objects.order_by('-id')
    serializer_class = ContactUsSerializer


class ConfigurationRetrieveView(RetrieveAPIView):
    serializer_class = ConfigurationSerializer

    def get_object(self):
        return Configuration.objects.order_by('-id').first()
