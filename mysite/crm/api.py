from rest_framework.views import APIView  # rest_framework
from rest_framework.response import Response  # rest_framework
from rest_framework.authtoken.views import ObtainAuthToken  # rest_framework
from rest_framework.authtoken.models import Token  # rest_framework
from rest_framework import status

from .serializers import *
from .models import *


# Token
class UserAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data, context={"request": request})
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(token.key)

class ControlVersionList(APIView):
    def get(self, request):
        model = ControlVersion.objects.all()
        serializer = ControlVersionSerializer(model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ControlVersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ControlVersionDetail(APIView):

    def get_ControlVersion(self, pk):
        try:
            model = ControlVersion.objects.get(hcode=pk)
            return model
        except ControlVersion.DoesNotExist:
            return

    def get(self, request, pk):
        # model = Hospitals.objects.filter(id=pk)
        # serializer = hospitalSerializer(model, many=True)
        # if serializer.data == []:
        try:
            model = ControlVersion.objects.get(hcode=pk)
        except ControlVersion.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = ControlVersionSerializer(model)  # ใช้ get ไม่ต้องใช่ many=True
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            model = ControlVersion.objects.get(hcode=pk)
        except ControlVersion.DoesNotExist:
            return Response("ControlVersion with {} is Not Found".format(pk), status=status.HTTP_404_NOT_FOUND)

        serializer = ControlVersionSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not self.get_ControlVersion(pk):
            return ("del ControlVersion with {} is Not Found".format(pk))
        model = ControlVersion.objects.get(hcode=pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


