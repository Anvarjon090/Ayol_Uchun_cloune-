from rest_framework import serializers
from apps.news.models import (
    Post,
    Event,
    Survey,
    Question,
    QuestionOption,
    Submission
)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "description", "card", "created_at", "updated_at"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "card",
            "datetime",
            "location_name",
            "longitude",
            "latitude",
            "created_at",
            "updated_at",
        ]


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id", "question", "title", "created_at", "updated_at"]


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "survey",
            "title",
            "type",
            "file",
            "options",
            "created_at",
            "updated_at",
        ]


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Survey
        fields = [
            "id",
            "course",
            "title",
            "description",
            "card",
            "questions",
            "created_at",
            "updated_at",
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "user",
            "question",
            "chosen_option",
            "text_answer",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        # chosen_option yoki text_answer kamida bittasi bo‘lishi kerak
        if not data.get("chosen_option") and not data.get("text_answer"):
            raise serializers.ValidationError(
                "Submission must contain either chosen_option or text_answer."
            )
        return data