from rest_framework import serializers, viewsets

from .models import City, Hotel


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Hotel
        fields = '__all__'
