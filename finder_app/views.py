# views.py
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Contact, StatusHistory
from .serializers import (
    ContactSerializer,
    StatusHistorySerializer,
)


class ContactListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            father_created = False
            mother_created = False

            father_national_id = data.get("father", None)
            mother_national_id = data.get("mother", None)

            father = Contact.objects.filter(national_id=father_national_id).first()
            mother = Contact.objects.filter(national_id=mother_national_id).first()

            if father_national_id and father is None:
                father = Contact.objects.create(
                    national_id=father_national_id, gender="m"
                )
                father_created = True

            if mother_national_id and mother is None:
                mother = Contact.objects.create(
                    national_id=mother_national_id, gender="f"
                )
                mother_created = True

            serializer.save(father=father, mother=mother)

            response_data = dict(serializer.data)
            response_data["father_created"] = father_created
            response_data["mother_created"] = mother_created

            headers = self.get_success_headers(response_data)
            return Response(
                response_data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ContactSearchView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'national_id']
