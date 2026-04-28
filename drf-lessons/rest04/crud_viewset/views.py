from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from crud.models import Watch
from crud.serializers import WatchSerializer


## ModelViewSet


# class WatchModelViewSet(viewsets.ModelViewSet):
#     serializer_class = WatchSerializer
#     queryset = Watch.objects.all()

class WatchViewSet(viewsets.ViewSet):
    serializer_class = WatchSerializer

    def get_object(self, pk):
        return get_object_or_404(Watch, pk=pk)

    # GET /watches/
    def list(self, request):
        queryset   = Watch.objects.all()
        serializer = WatchSerializer(queryset, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'count':  queryset.count(),
            'data':   serializer.data,
        })

    # POST /watches/
    def create(self, request):
        serializer = WatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status':  status.HTTP_201_CREATED,
            'data':    serializer.data,
            'message': 'Watch Created Successfully',
        }, status=status.HTTP_201_CREATED)

    # GET /watches/{pk}/
    def retrieve(self, request, pk=None):
        watch      = self.get_object(pk)
        serializer = WatchSerializer(watch)
        return Response({
            'status': status.HTTP_200_OK,
            'data':   serializer.data,
        })

    # PUT /watches/{pk}/
    def update(self, request, pk=None):
        watch      = self.get_object(pk)
        serializer = WatchSerializer(instance=watch, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': status.HTTP_200_OK,
            'data':   WatchSerializer(watch).data,
        })

    # PATCH /watches/{pk}/
    def partial_update(self, request, pk=None):
        watch      = self.get_object(pk)
        serializer = WatchSerializer(instance=watch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': status.HTTP_200_OK,
            'data':   WatchSerializer(watch).data,
        })

    # DELETE /watches/{pk}/
    def destroy(self, request, pk=None):
        self.get_object(pk).delete()
        return Response({
            'status':  status.HTTP_204_NO_CONTENT,
            'message': 'Watch Deleted',
        })