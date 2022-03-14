
from django import forms
from django.contrib.auth import forms as auth_forms
from .models import Ticket, Review
from django.forms.utils import ErrorList


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'image',
            'user',
        ]
        exclude = ['user']

        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image",
        }
        

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'headline',
            'rating',
            'body',
            'user',
            
        ]
        exclude = ['user']

        labels = {
            "headline": "Description",
            "rating": ("Note / 5"),
            "body": "Comments",
        }
        






