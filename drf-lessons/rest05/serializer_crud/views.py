from django.db.models import Q, Count
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response

from .models import Watch
from .serializers import WatchCreateSerializer, WatchUpdateSerializer, WatchListSerializer


class WatchCreateView(CreateAPIView):
    serializer_class = WatchCreateSerializer
    queryset = Watch.objects.all()

class WatchUpdateView(UpdateAPIView):
    serializer_class = WatchUpdateSerializer
    queryset = Watch.objects.all()


class WatchSearchView(ListAPIView):
    serializer_class = WatchListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        watches = Watch.objects.filter(
            Q(brand__icontains=query) |
            Q(country__icontains=query)
        )

        if min_price:
            watches = watches.filter(price__gte=min_price)
        if max_price:
            watches = watches.filter(price__lte=max_price)

        return watches

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'status': 'success',
            'result': serializer.data
        })