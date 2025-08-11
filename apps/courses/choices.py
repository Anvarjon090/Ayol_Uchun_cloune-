from django.db.models import TextChoices


class ProductTypeChoices(TextChoices):
    COURSE = "course", "Course"
    WEBINAR = "webinar", "Webinar"