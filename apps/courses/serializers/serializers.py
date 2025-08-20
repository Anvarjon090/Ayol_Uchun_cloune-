from rest_framework import serializers

from apps.courses.models import Category, Comment, Course, Lesson, Module, Webinar


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon", "created_at", "updated_at"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "module",
            "title",
            "description",
            "file",
            "duration",
            "created_at",
            "updated_at",
        ]


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)

    class Meta:
        model = Module
        fields = ["id", "course", "name", "icon", "lessons", "created_at", "updated_at"]


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    author = serializers.PrimaryKeyRelatedField(
        read_only=True
    )  # set in view from request.user
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "price",
            "card",
            "category",
            "category_id",
            "author",
            "rating",
            "average_rating",
            "modules",
            "created_at",
            "updated_at",
        ]


class WebinarSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Webinar
        fields = [
            "id",
            "title",
            "description",
            "price",
            "card",
            "category",
            "category_id",
            "author",
            "datetime",
            "rating",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "course",
            "webinar",
            "text",
            "rating",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        # at least one of course or webinar must be provided
        course = data.get("course") or getattr(self.instance, "course", None)
        webinar = data.get("webinar") or getattr(self.instance, "webinar", None)
        if not course and not webinar:
            raise serializers.ValidationError(
                "Comment must be related to either a course or a webinar."
            )
        # prevent both being provided (optional — if you want exclusivity)
        if course and webinar:
            raise serializers.ValidationError(
                "Comment can be related to only one of course or webinar."
            )
        return data
