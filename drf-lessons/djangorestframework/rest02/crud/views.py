from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Watch
from .serializers import WatchSerializer



# Create your views here.

class WatchListView(APIView):
    def get(self, request):
        soatlar = Watch.objects.all()
        serializer = WatchSerializer(soatlar, many=True)
        return Response(serializer.data)


class WatchCreateView(APIView):
    def post(self, request):
        serializer = WatchSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class WatchDetailView(APIView):
    def get(self, request, pk):
        watch = Watch.objects.filter(pk=pk).first()
        if watch is None:
            raise NotFound({'message':'Soat mavjud emas'})
        serializer = WatchSerializer(watch)
        return Response(serializer.data)

class WatchUpdateView(APIView):
    def put(self, request, pk):
        watch = Watch.objects.filter(pk=pk).first()
        if watch is None:
            raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
        serializer = WatchSerializer(data=request.data, instance=watch)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


    def patch(self, request, pk):
        watch = Watch.objects.filter(pk=pk).first()
        if watch is None:
            raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
        serializer = WatchSerializer(data=request.data, instance=watch, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class WatchDeleteView(APIView):
    def delete(self, request, pk):
        watch = Watch.objects.filter(pk=pk).first()
        if watch is None:
            raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
        watch.delete()
        return Response({'message': 'kitob ochirildi', 'status': status.HTTP_200_OK})

##### Boshqacha usuli

#
# class WatchListCreateView(APIView):
#     def get(self, request):
#         soatlar = Watch.objects.all()
#         serializer = WatchSerializer(soatlar, many=True)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         watch = Watch.objects.filter(pk=pk).first()
#         if watch is None:
#             raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
#         serializer = WatchSerializer(data=request.data, instance=watch)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#
# class WatchDetailUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         watch = Watch.objects.filter(pk=pk).first()
#         if watch is None:
#             raise NotFound({'message':'Soat mavjud emas'})
#         serializer = WatchSerializer(watch)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         watch = Watch.objects.filter(pk=pk).first()
#         if watch is None:
#             raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
#         serializer = WatchSerializer(data=request.data, instance=watch)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#     def patch(self, request, pk):
#         watch = Watch.objects.filter(pk=pk).first()
#         if watch is None:
#             raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
#         serializer = WatchSerializer(data=request.data, instance=watch, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#     def delete(self, request, pk):
#         watch = Watch.objects.filter(pk=pk).first()
#         if watch is None:
#             raise NotFound({'message':'Soat mavjud emas', 'status': status.HTTP_400_BAD_REQUEST})
#         watch.delete()
#         return Response({'message': 'kitob ochirildi', 'status': status.HTTP_200_OK})
#
#


