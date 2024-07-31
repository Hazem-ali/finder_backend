# views.py
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Suspect, SuspectPhoto
from .serializers import SuspectSerializer, SuspectPhotoSerializer
from .permissions import IsSupervisorOrInformerOrReadOnly
import json

class SuspectCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SuspectSerializer

    def get_queryset(self):
        if self.request.user.is_supervisor:
            return Suspect.objects.all()
        return Suspect.objects.filter(informer=self.request.user.id)

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            suspect=serializer.save(informer=request.user)

            photos_files = request.data.getlist('photos_data')
            print(photos_files)
            
            for photo_file in photos_files:
                SuspectPhoto.objects.create(suspect=suspect, photo=photo_file)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuspectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsSupervisorOrInformerOrReadOnly]
    serializer_class = SuspectSerializer
    queryset = Suspect.objects.all()


class SuspectPhotoAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSupervisorOrInformerOrReadOnly]
    serializer_class = SuspectPhotoSerializer
    queryset = SuspectPhoto.objects.all()
