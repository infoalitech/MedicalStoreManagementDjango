from django.db import models

from accounts.models import Ledger
# Create your models here.

class Customer(models.Model):
    balance_type = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )
    def __str__(self):
        return self.name 

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,  null=True, blank=True)
    phone = models.CharField(max_length=200,  null=True, blank=True)
    cell = models.CharField(max_length=200,  null=True, blank=True)
    email = models.CharField(max_length=200,  null=True, blank=True)
    initial_balance = models.IntegerField(  null=True, blank=True)
    initial_balance_db = models.CharField(max_length=1, choices=balance_type,default='D')
    created_date = models.DateTimeField(auto_now=True)
    ledger = models.OneToOneField(Ledger,on_delete=models.CASCADE,  null=True, blank=True)