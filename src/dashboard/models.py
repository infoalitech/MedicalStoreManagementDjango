from django.db import models

# Create your models here.


class Setting(models.Model):
    def __str__(self):
        return self.name 
    name = models.CharField(max_length=200)
    value = models.IntegerField(default=0)

class CompanyData(models.Model):
    def __str__(self):
        return self.name 
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
