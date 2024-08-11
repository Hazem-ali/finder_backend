# serializers.py
from rest_framework import serializers
from .models import Suspect, SuspectPhoto
from user_app.serializers import UserSerializer


class SuspectPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuspectPhoto
        fields = ["photo", "suspect", "created_at"]
        extra_kwargs = {"created_at": {"read_only": True}}


class SuspectSerializer(serializers.ModelSerializer):
    photo_details = SuspectPhotoSerializer(many=True ,read_only=True)
    informer = serializers.StringRelatedField()

    class Meta:
        model = Suspect
        fields = [
            "id",
            "name",
            "status",
            "where",
            "time",
            "national_id",
            "notes",
            "informer",
            "photo_details",
        ]
