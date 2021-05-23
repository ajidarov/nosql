from django import forms
from django.forms import fields, widgets
from .models import *

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']