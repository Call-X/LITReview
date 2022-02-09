from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    type = 'ticket'
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=2048, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    completed = models.BooleanField(default=False)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


""" class UserFollows(models.Model):
    class Meta:
        model = UserFollows
        fields = ['user', 'followed_user']
        labels = {'followed_user': 'Utilisateur à suivre :'}
        exclude = ['user']
        widgets = {'followed_user': forms.TextInput}

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', ) """
