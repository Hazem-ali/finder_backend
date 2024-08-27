# views.py
from weakref import finalize
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Contact, StatusHistory
from .serializers import (
    ContactCreateSerializer,
    ContactViewSerializer,
    StatusHistorySerializer,
)


class ContactListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ContactCreateSerializer
    queryset = Contact.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():

            father_national_id = data.get("father", None)
            mother_national_id = data.get("mother", None)

            father = Contact.objects.filter(national_id=father_national_id).first()
            mother = Contact.objects.filter(national_id=mother_national_id).first()

            if father_national_id and father is None:
                father = Contact.objects.create(
                    national_id=father_national_id, gender="m"
                )
            if mother_national_id and mother is None:
                mother = Contact.objects.create(
                    national_id=mother_national_id, gender="f"
                )

            serializer.save(father=father, mother=mother)

            # serializer.save(user=request.user)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ContactViewSerializer
    queryset = Contact.objects.all()
