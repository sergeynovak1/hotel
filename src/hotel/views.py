from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Hotel
from .serializers import HotelSerializer


class HotelListAPIView(ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        queryset = Hotel.objects.all()

        city_id = self.request.GET.get('city_id')
        from_id = self.request.GET.get('from_id')
        limit = self.request.GET.get('limit')

        if city_id:
            queryset = queryset.filter(city_id=city_id)
        if from_id:
            queryset = queryset.filter(id__gt=from_id)
        if limit:
            if not limit.isdigit():
                raise ValueError("Limit must be a valid integer.")
            queryset = queryset[:int(limit)]

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
