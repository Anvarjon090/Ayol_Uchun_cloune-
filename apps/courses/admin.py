from django.contrib import admin

from apps.courses.models import Category, Comment, Course, Lesson, Module, Webinar


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category__name", "price", "rating")
    list_display_links = ("id", "title")
    list_filter = ("category",)
    search_fields = ("title", "category__name")
    ordering = ("-created_at",)


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category__name", "price", "rating")
    list_display_links = ("id", "title")
    list_filter = ("category",)
    search_fields = ("title", "category__name")
    ordering = ("-created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "icon")
    list_display_links = ("id", "name")
    ordering = ("-created_at",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course__title", "icon")
    list_display_links = ("id", "name")
    list_filter = ("course",)
    search_fields = ("name", "course__title")
    ordering = ("-created_at",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "module__name", "duration", "created_at")
    list_display_links = ("id", "title")
    list_filter = ("module",)
    search_fields = ("title", "module__name")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user__username", "course__title", "rating")
    list_display_links = ("id", "user__username")
    search_fields = ("user__username", "lesson__title")
    ordering = ("-created_at",)
