from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Course(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )
    card = models.FileField(
        upload_to="courses", null=True, blank=True, verbose_name=_("Card Image")
    )
    category = models.ForeignKey(
        "courses.Category",
        on_delete=models.RESTRICT,
        related_name="courses",
        verbose_name=_("Category"),
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.RESTRICT,
        related_name="courses",
        verbose_name=_("Author"),
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Rating"),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")


class Webinar(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    card = models.FileField(
        upload_to="webinars", null=True, blank=True, verbose_name=_("Card Image")
    )
    category = models.ForeignKey(
        "courses.Category",
        on_delete=models.RESTRICT,
        related_name="webinars",
        verbose_name=_("Category"),
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.RESTRICT, related_name="webinars"
    )
    datetime = models.DateTimeField(verbose_name=_("Datetime"))
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Rating"),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Webinar")
        verbose_name_plural = _("Webinars")


class Category(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    icon = models.ImageField(
        upload_to="categories", null=True, blank=True, verbose_name=_("Icon")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Module(BaseModel):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name=_("Course"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    icon = models.ImageField(
        upload_to="modules", null=True, blank=True, verbose_name=_("Icon")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")


class Lesson(BaseModel):
    module = models.ForeignKey(
        "courses.Module",
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Module"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    file = models.FileField(
        upload_to="lessons", null=True, blank=True, verbose_name=_("File")
    )
    duration = models.DurationField(verbose_name=_("Duration"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")


class Comment(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User"),
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Course"),
        null=True,
        blank=True,
    )
    webinar = models.ForeignKey(
        "courses.Webinar",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Webinar"),
        null=True,
        blank=True,
    )
    text = models.TextField(verbose_name=_("Text"))
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Rating"),
    )

    def __str__(self):
        return f"{self.user}: {self.text[:10]}..."

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
