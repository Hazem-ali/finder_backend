# serializers.py
from rest_framework import serializers
from .models import Contact, StatusHistory


def is_valid_relationship(contact, relationship):
    if (relationship == "father" and contact.gender == "m") or (
        relationship == "mother" and contact.gender == "f"
    ):
        return True
    return False


class ContactSerializer(serializers.ModelSerializer):
    father = serializers.CharField()
    mother = serializers.CharField()
    full_name = serializers.SerializerMethodField()


    def get_full_name(self, obj):
        # Return the full name (4 names)
        full_name = ""

        full_name += obj.name
        parent = obj
        i = 0
        while i < 3:
            parent = parent.father
            if parent and parent.name:
                full_name += f" {parent.name}"
            else:
                break

        return full_name





    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "full_name",
            "father",
            "mother",
            "national_id",
            "user",
            "image",
            "dob",
            "gender",
            "status",
        ]

    def validate(self, data):
        father_national_id = data.get("father")
        mother_national_id = data.get("mother")

        father = None
        mother = None

        if father_national_id:
            father = Contact.objects.filter(national_id=father_national_id).first()

            if father and father.gender and not is_valid_relationship(father, "father"):
                raise serializers.ValidationError(
                    {"father": "Error, You entered a female as a father."}
                )

        if mother_national_id:
            mother = Contact.objects.filter(national_id=mother_national_id).first()

            if mother and mother.gender and not is_valid_relationship(mother, "mother"):
                raise serializers.ValidationError(
                    {"mother": "Error, You entered a male as a mother."}
                )

        data["father"] = father
        data["mother"] = mother
        return data


class StatusHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusHistory
        fields = [
            "name",
            "national_id",
            "father",
            "mother",
            "user",
            "image",
            "dob",
            "gender",
            "status",
        ]
