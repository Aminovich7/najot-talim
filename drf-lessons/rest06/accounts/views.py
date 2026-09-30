from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import SignupSerializer
# Create your views here.



class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response({
                "message":"User  created",
                "user": serializer.data
            })