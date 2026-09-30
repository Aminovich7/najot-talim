from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .models import Tool
from .serializers import ToolSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView


class ToolListView(ListAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'status': 200,
            'message': 'Ro`yxat!',
            'data': serializer.data
        }

        return Response(data)


class ToolCreateView(CreateAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = {
            'status': 201,
            'message': 'Created!',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED)
class ToolDetailView(RetrieveAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = {
            'status': 200,
            'message': 'Detail!',
            'data': serializer.data
        }

        return Response(data)



class ToolDeleteView(DestroyAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def delete(self, request, *args, **kwargs):
        data = {
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Deleted',
        }

        super().delete(request, *args, **kwargs)

        return Response(data)



class ToolUpdateView(UpdateAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            'status': 200,
            'message': 'Updated!',
            'data': serializer.data
        }

        return Response(data)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

