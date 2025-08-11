from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import Interest, UserCourse, UserWebinar
from apps.courses.models import Course, Webinar

User = get_user_model()


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "phone_number", "username", "email",
            "first_name", "last_name", "avatar", "bio",
            "is_active", "is_confirmed", "interests"
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ["id", "user", "course"]


class UserWebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWebinar
        fields = ["id", "user", "webinar"]