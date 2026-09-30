from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from crud.models import Watch
from crud.serializers import WatchSerializer


class WatchGenericApiView(GenericAPIView):
    serializer_class = WatchSerializer
    queryset = Watch.objects.all()


    def get_object(self, pk):
        return get_object_or_404(Watch, pk=pk)



    def get(self, request, pk=None):
        if pk:
            return Response({
                'status': status.HTTP_200_OK,
                'data': self.get_serializer(self.get_object(pk)).data
            })

        return Response({
            'status': status.HTTP_200_OK,
            'count': self.get_queryset().count(),
            'data': self.get_serializer(self.get_queryset(), many=True).data,
        })

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'data': serializer.data,
                'message': 'Watch Created Successfully'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Watch Deleted'
        })

    def put(self, request, pk):
        watch = self.get_object(pk)
        serializer = self.get_serializer(data=request.data, instance=watch)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': status.HTTP_200_OK,
            'data': self.get_serializer(watch).data
        })

    def patch(self, request, pk):
        watch = self.get_object(pk)
        serializer = self.get_serializer(data=request.data, instance=watch, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': status.HTTP_200_OK,
            'data': self.get_serializer(watch).data
        })

    