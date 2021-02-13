from django.db import models
from accounts.models import Ledger
from supplier.models import Supplier
# Create your models here.

class Product_Types(models.Model):

    def __str__(self):
        return self.name 

    name = models.CharField(max_length=200)

class Product(models.Model):
    active_inactive = (
        ('0', 'Active'),
        ('1', 'Inactive'),
    )
    balance_type = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )
    product_type = (
        ('T', 'Tablet'),
        ('S', 'Syrup'),
        ('I', 'Injection'),
        ('C', 'Common')
    )
    def __str__(self):
        return self.name +' - ' + self.code +' - '+ self.mg
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    mg = models.CharField(max_length=200)
    tablets = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    # initial Stock table
    s_pack = models.IntegerField(default=0)
    s_tablet = models.IntegerField(default=0)
    # stock table
    stock_pack = models.IntegerField(default=0)
    stock_tablet = models.IntegerField(default=0)
    # purchase
    purchase_pack = models.IntegerField(default=0)
    purchase_tablet = models.IntegerField(default=0)
    # purchase_return
    purchase_return_pack = models.IntegerField(default=0)
    purchase_return_tablet = models.IntegerField(default=0)
    # sale
    sale_pack = models.IntegerField(default=0)
    sale_tablet = models.IntegerField(default=0)
    # sale_return
    sale_return_pack = models.IntegerField(default=0)
    sale_return_tablet = models.IntegerField(default=0)    
    # used
    used_pack = models.IntegerField(default=0)
    used_tablet = models.IntegerField(default=0)

    active = models.CharField(max_length=1, choices=active_inactive,default='0')
    type_id = models.CharField(max_length=1, choices=product_type,default='T')
    ledger = models.OneToOneField(Ledger,on_delete=models.CASCADE,  null=True, blank=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE, null=True, blank=True)
    initial_balance = models.IntegerField(  null=True, blank=True)
    
    initial_balance_db = models.CharField(max_length=1, choices=balance_type,default='D')
    created_date = models.DateTimeField('date')
    