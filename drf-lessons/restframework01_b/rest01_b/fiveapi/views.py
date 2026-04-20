from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from .models import Watch
from .serializers import WatchSerializer


# Create your views here.
@api_view(['GET'])

def get_list(request):
    watch = Watch.objects.all()
    serializer = WatchSerializer(watch, many=True)

    return Response(serializer.data)


@api_view(['POST'])

def create(request):
    serializer = WatchSerializer(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    raise ValidationError({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Xato malumot'})


@api_view(['PUT'])

def update_put(request, pk):
    watch = Watch.objects.filter(pk=pk).first()
    serializer = WatchSerializer(data= request.data, instance=watch)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Yangilandi',
            'data': serializer.data

        })



@api_view(['PATCH'])

def update_patch(request, pk):
    watch = Watch.objects.filter(pk=pk).first()
    serializer = WatchSerializer(data= request.data, instance=watch, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Yangilandi',
            'data': serializer.data

        })


@api_view(['DELETE'])

def delete(request, pk):
    watch = Watch.objects.filter(pk = pk).first()
    watch.delete()
    return Response({
        'status': status.HTTP_204_NO_CONTENT,
        'message': 'Deleted'
    })


