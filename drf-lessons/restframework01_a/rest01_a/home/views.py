from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import WatchSerializer
from .models import Watch

# Create your views here.

@api_view(['GET', 'POST'])
def list_create(request):
    if request.method == 'GET':

        watch = Watch.objects.all()
        serializer = WatchSerializer(watch, many=True)


        data = {
            'status': 'New',
            'message': 'Watches List',
            'count': len(serializer.data),
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)


    if request.method == 'POST':
        serializer = WatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        raise ValidationError({"status": status.HTTP_400_BAD_REQUEST, "message": 'Xato malumot'})


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])

def update_detail_destroy(request, pk):
    if request.method == 'PUT':
        watch = Watch.objects.filter(pk=pk).first()
        serializer = WatchSerializer(data=request.data, instance=watch)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Yangilandi',
                'data': serializer.data

            })

    if request.method == 'PATCH':
        watch = Watch.objects.filter(pk=pk).first()
        serializer = WatchSerializer(data=request.data, instance=watch, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Yangilandi',
                'data': serializer.data

            })
    if request.method == 'GET':
        watch = Watch.objects.filter(pk=pk).first()
        serializer = WatchSerializer(watch)

        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Detail',
            'data': serializer.data

        })

    if request.method == 'DELETE':
        watch = Watch.objects.filter(pk=pk).first()
        watch.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Deleted',
        })
