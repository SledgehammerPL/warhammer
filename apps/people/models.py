from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.game import models as game_models

class Person(AbstractUser):
    username = None
    created = models.DateTimeField(auto_now_add=True)
    password = models.CharField(_('password'), max_length=128, blank=True, null=True)
    email = models.EmailField(unique=True,)
    selected_character = models.ForeignKey(game_models.Character, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "people"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
