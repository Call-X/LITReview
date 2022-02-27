
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

        Widget = {
            'body' : forms.Textarea(attrs={'col' : 40, 'rows' : 15})
        }
        labels = {
            "headline": "Description",
            "rating": ("Note / 5"),
            "body": "Comments",
        }




class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])