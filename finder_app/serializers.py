# serializers.py
from rest_framework import serializers
from .models import Contact, StatusHistory


def is_valid_relationship(contact, relationship):
    if (relationship == "father" and contact.gender == "m") or (
        relationship == "mother" and contact.gender == "f"
    ):
        return True
    return False


class ContactCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "father",
            "mother",
            "national_id",
            "user",
            "photo",
            "dob",
            "gender",
            "status",
        ]

    def validate(self, data):
        print(dict(data))
        father = Contact.objects.filter(national_id=data.get("father", None)).first()
        mother = Contact.objects.filter(national_id=data.get("mother", None)).first()
        if father and father.gender:
            if not is_valid_relationship(father, "father"):
                raise serializers.ValidationError(
                    "Error, You entered a female as a father"
                )
        if mother and mother.gender:
            if not is_valid_relationship(mother, "mother"):
                raise serializers.ValidationError(
                    "Error, You entered a male as a mother"
                )

        return data


class ContactViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            "name",
            "national_id",
            "father",
            "mother",
            "user",
            "photo",
            "dob",
            "gender",
            "status",
        ]


class StatusHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusHistory
        fields = [
            "name",
            "national_id",
            "father",
            "mother",
            "user",
            "photo",
            "dob",
            "gender",
            "status",
        ]
