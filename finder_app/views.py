# views.py
import requests
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from finder_backend.settings import ML_URL
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsSearcher
from .models import Contact, StatusHistory
from .serializers import (
    ContactSerializer,
    StatusHistorySerializer,
    ImageUploadSerializer,
)

import requests
from rest_framework import generics, status
from rest_framework.response import Response


class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(data.get("image"))

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():

            files = {"image": data["image"]}
            try:
                flask_response = requests.post(f"{ML_URL}/images/encode", files=files)
                print("FUCKIN========================")
                print(f"{flask_response}")
                flask_response.raise_for_status()

            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": f"Error communicating with ML model: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            encoded_image = flask_response.json()
            if not encoded_image or encoded_image == -1:
                return Response(
                    {"error": "Image has no faces"}, status=status.HTTP_400_BAD_REQUEST
                )

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

            contact = serializer.save(father=father, mother=mother)

            image_encoding_data = {"id": contact.id, "encoded_image": encoded_image}

            try:
                flask_save_response = requests.post(
                    f"{ML_URL}/contacts/save", json=image_encoding_data
                )
                flask_save_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": f"Error communicating with ML model: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

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
    # permission_classes = [IsSearcher]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "national_id"]


class ContactImageSearchView(APIView):
    # permission_classes = [IsSearcher]

    def post(self, request, *args, **kwargs):
        image_serializer = ImageUploadSerializer(data=request.data)

        if image_serializer.is_valid():
            image_file = request.data.get("image")
            # Prepare the file for forwarding
            files = {"image": image_file}

            try:
                flask_response = requests.post(ML_URL, files=files)
                flask_response.raise_for_status()
                found_ids = flask_response.json()

                if found_ids:
                    contacts = Contact.objects.filter(pk__in=found_ids)
                    contact_serializer = ContactSerializer(
                        contacts, many=True, context={"request": request}
                    )
                    print("contacts: ", contacts)
                    print("contact_serializer.data: ", contact_serializer.data)

                    return Response(contact_serializer.data, status=status.HTTP_200_OK)
                return Response([], status=status.HTTP_204_NO_CONTENT)

            except requests.exceptions.RequestException as e:
                print(f"Error communicating with Flask server: {e}")
                return Response(
                    {"message": "Error communicating with Flask server"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
