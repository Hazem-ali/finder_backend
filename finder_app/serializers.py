# serializers.py
from rest_framework import serializers
from .models import Contact, StatusHistory


def is_valid_relationship(contact, relationship):
    if (relationship == "father" and contact.gender == "m") or (
        relationship == "mother" and contact.gender == "f"
    ):
        return True
    return False


class ParentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Contact
        fields = ["id", "name", "image", "national_id"]



class ChildSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Contact
        fields = ["id", "name", "image", "national_id"]



class ContactSerializer(serializers.ModelSerializer):
    father = ParentSerializer(read_only=True)
    mother = ParentSerializer(read_only=True)
    children = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = None
        if obj.gender == "m":
            children = Contact.objects.filter(father=obj)
        elif obj.gender == "f":
            children = Contact.objects.filter(mother=obj)

        if children:
            return ChildSerializer(children, many=True).data
        return None


    def get_full_name(self, obj):
        # Return the full name (up to 4 names including father/grandfather names)
        full_name = obj.name
        parent = obj.father  # Start with the father
        i = 0

        while parent and i < 3:
            if parent.name:
                full_name += f" {parent.name}"
            parent = parent.father  # Move to the next father in the chain
            i += 1

        return full_name

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "full_name",
            "father",
            "mother",
            "children",
            "national_id",
            "user",
            "image",
            "dob",
            "gender",
            "status",
        ]
        # depth=1

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
        fields = '__all__'


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
