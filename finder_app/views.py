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

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():

            files = {"image": data["image"]}
            try:
                flask_response = requests.post(f"{ML_URL}/images/encode", files=files)
                flask_response.raise_for_status()

            except requests.exceptions.RequestException as e:
                return Response(
                    {"detail": f"Error communicating with ML model: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            encoded_image = flask_response.json()
            if not encoded_image or encoded_image == -1:
                return Response(
                    {"detail": "Cannot detect faces. Please try a different image"}, status=status.HTTP_400_BAD_REQUEST
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
                    {"detail": f"Error communicating with ML model: {e}"},
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

    def put(self, request, *args, **kwargs):
        contact = Contact.objects.get(id=kwargs.get("pk"))

        father_national_id = request.data.get("father", None)
        mother_national_id = request.data.get("mother", None)
        if father_national_id == "undefined":
            father_national_id = None
        if mother_national_id == "undefined":
            mother_national_id = None

        father = Contact.objects.filter(national_id=father_national_id).first()
        mother = Contact.objects.filter(national_id=mother_national_id).first()

        if father_national_id and father is None:
            father = Contact.objects.create(national_id=father_national_id, gender="m")

        if mother_national_id and mother is None:
            mother = Contact.objects.create(national_id=mother_national_id, gender="f")

        if (father and father.gender != "m") or (mother and mother.gender != "f"):
            return Response(
                {
                    "detail": "Make sure the parent id matches the gender (eg. Father is male)"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            contact,
            data=request.data,
        )
        if serializer.is_valid(raise_exception=True):
            files = {"image": request.data["image"]}
            try:
                flask_response = requests.post(f"{ML_URL}/images/encode", files=files)
                flask_response.raise_for_status()

            except requests.exceptions.RequestException as e:
                return Response(
                    {"detail": f"Error communicating with ML model: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            encoded_image = flask_response.json()
            if not encoded_image or encoded_image == -1:
                return Response(
                    {"detail": "Cannot detect faces. Please try a different image"}, status=status.HTTP_400_BAD_REQUEST
                )

            image_encoding_data = {"id": contact.id, "encoded_image": encoded_image}

            try:
                flask_save_response = requests.post(
                    f"{ML_URL}/contacts/save", json=image_encoding_data
                )
                flask_save_response.raise_for_status()

            except requests.exceptions.RequestException as e:
                return Response(
                    {"detail": f"Error communicating with ML model: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        contact_status = request.data.get("status", "")
        print(f"Status: {contact_status} and {contact.status}")

        if contact_status != contact.status:

            StatusHistory.objects.create(contact=contact, status=contact_status)
            print(
                f"created successfuly for contact {contact} with status {contact_status}"
            )
        serializer.save(father=father, mother=mother)

        return Response(serializer.data)


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
                if status.is_server_error(flask_response.status_code):
                    return Response(
                        {
                            "message": "Cannot detect faces. Please try a different image"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                found_ids_dict = flask_response.json()
                if found_ids_dict:
                    contacts = Contact.objects.filter(pk__in=found_ids_dict.keys())

                    contact_serializer = ContactSerializer(
                        contacts, many=True, context={"request": request}
                    )

                    # Add confidence to each contact
                    contact_data = contact_serializer.data
                    for contact in contact_data:
                        contact_id = str(contact["id"])
                        contact["confidence"] = round(
                            100 * found_ids_dict.get(contact_id), 2
                        )

                    contact_data.sort(key=lambda c: c["confidence"], reverse=True)
                    return Response(contact_data, status=status.HTTP_200_OK)
                return Response([], status=status.HTTP_204_NO_CONTENT)

            except requests.exceptions.RequestException as e:
                print(f"Error communicating with Flask server: {e}")
                return Response(
                    {
                        "message": "Cannot detect faces. Please try a different image"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {
                "message": "Cannot detect faces. Please try a different image"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ContactStatusListAPIView(generics.ListAPIView):

    serializer_class = StatusHistorySerializer

    def get_queryset(self):
        return StatusHistory.objects.filter(contact__id=self.kwargs["pk"]).order_by(
            "-created_at"
        )
