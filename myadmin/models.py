from django.db import models

# Create your models here.
class AdminModel(models.Model):
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=100)