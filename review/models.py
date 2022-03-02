from xml.etree.ElementTree import Comment
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

import review



class Ticket(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=2048, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    completed = models.BooleanField(default=False)

    def ___str___(self):
        return self.title
    

    def is_already_reviewed(self, user):
        if self.user == user:
            return True

        return Review.objects.filter(ticket=self, user=user).exists()
        

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

    def ___str___(self):
        return self.headline

    @classmethod
    def get_rating_range(cls):
        return range(5)


