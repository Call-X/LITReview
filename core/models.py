from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        to='core.User', blank=True,)

    def followed_by(self):
        return User.objects.filter(following=self)
