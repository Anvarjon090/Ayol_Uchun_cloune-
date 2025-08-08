from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.choices import ReasonDeleteChoices
from apps.users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    phone_number = models.CharField(
        unique=True,
        max_length=50,  # Increased to accommodate suffix
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
        verbose_name=_("Phone number"),
    )
    password = models.CharField(max_length=128, verbose_name=_("Password"))
    username = models.CharField(max_length=30, verbose_name=_("Username"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    first_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name=_("Last name")
    )
    avatar = models.ImageField(
        upload_to="avatars", null=True, blank=True, verbose_name=_("Avatar")
    )
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))
    reason_delete_choices = models.CharField(
        choices=ReasonDeleteChoices.choices,
        null=True,
        blank=True,
        verbose_name=_("Reason Delete Choice"),
    )
    reason_delete_str = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Reason Delete String")
    )

    interests = models.ManyToManyField("Interest", blank=True)
    courses_purchased = models.ManyToManyField(
        "courses.Course", through="UserCourse", related_name="purchased_by", blank=True
    )
    webinars_purchased = models.ManyToManyField(
        "courses.Webinar",
        through="UserWebinar",
        related_name="purchased_by",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "username"
    ]  # username is also required, we'll ask while registration

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                condition=models.Q(is_deleted=False),
                name="unique_active_username",
            ),
        ]

    def delete_account(self):
        """Soft delete user account"""
        from django.utils import timezone

        timestamp = int(timezone.now().timestamp())

        # Bypass validation by saving with update_fields
        self.phone_number = f"{self.phone_number}_deleted_{timestamp}"
        self.is_deleted = True
        self.save(update_fields=["phone_number", "is_deleted"])


class Interest(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Interest")
        verbose_name_plural = _("Interests")


class UserCourse(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, verbose_name=_("Course")
    )

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = _("User course")
        verbose_name_plural = _("User courses")
        unique_together = ("user", "course")  # Prevent duplicate purchases


class UserWebinar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    webinar = models.ForeignKey(
        "courses.Webinar", on_delete=models.CASCADE, verbose_name=_("Webinar")
    )

    def __str__(self):
        return f"{self.user} - {self.webinar}"

    class Meta:
        verbose_name = _("User webinar")
        verbose_name_plural = _("User webinars")
        unique_together = ("user", "webinar")  # Prevent duplicate purchases
