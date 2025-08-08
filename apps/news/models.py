from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.news.choices import QuestionTypeChoices


class Post(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    card = models.ImageField(
        upload_to="posts", null=True, blank=True, verbose_name=_("Card Image")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class Event(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    card = models.ImageField(
        upload_to="events", null=True, blank=True, verbose_name=_("Card Image")
    )
    datetime = models.DateTimeField(verbose_name=_("Datetime"))
    location_name = models.CharField(max_length=255, verbose_name=_("Location Name"))
    longitude = models.FloatField(verbose_name=_("Longitude"))
    latitude = models.FloatField(verbose_name=_("Latitude"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class Survey(BaseModel):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        related_name="surveys",
        null=True,
        blank=True,
        verbose_name=_("Course"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    card = models.ImageField(
        upload_to="surveys", null=True, blank=True, verbose_name=_("Card Image")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")


class Question(BaseModel):
    survey = models.ForeignKey(
        "news.Survey",
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Survey"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    type = models.CharField(
        choices=QuestionTypeChoices.choices, max_length=30, verbose_name=_("Type")
    )
    file = models.FileField(
        upload_to="questions", null=True, blank=True, verbose_name=_("File")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class QuestionOption(BaseModel):
    question = models.ForeignKey(
        "news.Question",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("Question"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Question Option")
        verbose_name_plural = _("Question Options")


class Submission(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name=_("User"),
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name=_("Question"),
    )
    chosen_option = models.ForeignKey(
        "news.QuestionOption",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="submissions",
        verbose_name=_("Chosen Option"),
    )
    text_answer = models.TextField(null=True, blank=True, verbose_name=_("Text Answer"))

    def __str__(self):
        return f"{self.user} - {self.question}"

    class Meta:
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")
