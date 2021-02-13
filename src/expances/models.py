from django.db import models

# Create your models here.
from accounts.models import Ledger

class Expance(models.Model):
    balance_type = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )
    def __str__(self):
        return self.name 

    name = models.CharField(max_length=200)
    initial_balance = models.IntegerField(  null=True, blank=True)
    initial_balance_db = models.CharField(max_length=1, choices=balance_type,default='D')
    created_date = models.DateTimeField(auto_now=True)
    ledger = models.OneToOneField(Ledger,on_delete=models.CASCADE,  null=True, blank=True)