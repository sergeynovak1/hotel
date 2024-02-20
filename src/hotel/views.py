from typing import Union, Any

from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status

from .models import Hotel
from .serializers import HotelSerializer


class HotelListAPIView(ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Hotel.objects.all()

        city_id: Union[str, None] = self.request.GET.get('city_id')
        from_id: Union[str, None] = self.request.GET.get('from_id')
        limit: Union[str, None] = self.request.GET.get('limit')

        if city_id:
            if not city_id.isdigit():
                raise ValueError("City_id must be a valid integer.")
            queryset = queryset.filter(city_id=city_id)
        if from_id:
            if not from_id.isdigit():
                raise ValueError("From_id must be a valid integer.")
            queryset = queryset.filter(id__gt=from_id)
        if limit:
            if not limit.isdigit():
                raise ValueError("Limit must be a valid integer.")
            queryset = queryset[:int(limit)]

        return queryset

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
