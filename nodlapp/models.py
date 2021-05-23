# from django.db import models
from django.contrib.auth.models import User
from django.db import models as modls
from djongo import models
from django import forms
from django.urls import reverse
import uuid
import os


class Groups(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10)
    students = models.ArrayReferenceField( to = User, related_name = '+')
    def __str__(self):
            return self.name

class Subject(models.Model):
    id = modls.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    groups = models.ArrayReferenceField(to = Groups, related_name = '+')
    
    def __str__(self):
            return self.title



class Week(models.Model):
    id = modls.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    material = models.FileField(upload_to='source_files')
    last_upload = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
            return self.subject.title +"_"+ self.title
    


class Submission(models.Model):
    id = modls.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submission_files')
    last_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.file.name)
