from django.contrib import admin

from apps.news.models import Post, Question, QuestionOption, Submission, Survey


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
    ordering = ("-created_at",)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
    ordering = ("-created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "survey__title", "created_at")
    list_display_links = ("id", "title")
    list_filter = ("survey", "created_at", "updated_at")
    search_fields = ("title", "survey__title")
    ordering = ("-created_at",)


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "question", "created_at")
    list_display_links = ("id", "title")
    list_filter = ("question", "created_at", "updated_at")
    search_fields = ("title", "question__title")
    ordering = ("-created_at",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user__username", "question__title", "created_at")
    list_display_links = ("id", "user__username")
    search_fields = ("user__username", "question__title")
    ordering = ("-created_at",)
