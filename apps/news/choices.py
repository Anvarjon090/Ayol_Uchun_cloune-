from django.db.models import TextChoices


class QuestionTypeChoices(TextChoices):
    SINGLE_CHOICE = "single_choice", "Single Choice"
    MULTI_CHOICE = "multi_choice", "Multi Choice"
    OPEN_ANSWER = "open_answer", "Open Answer"
