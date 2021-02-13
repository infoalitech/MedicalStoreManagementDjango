from django.db import models

# Create your models here.



class Group(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)

class Ledger_Type(models.Model):
    def __str__(self):
        return self.name 
    name = models.CharField(max_length=200)

class Ledger(models.Model):
    balance_type = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )
    def __int__(self):
        return self.balance
    balance = models.IntegerField(default=0)
    balance_dc = models.CharField(max_length=1, choices=balance_type,default='D')
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    Ledger_Type = models.ForeignKey(Ledger_Type,on_delete=models.CASCADE)

class Entry_Type(models.Model):
    def __str__(self):
        return self.name 
    name = models.CharField(max_length=200)

class Entry(models.Model):
    def __str__(self):
        return self.invoice_code 
    invoice_code = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    dr_total = models.IntegerField(default=0)
    cr_total = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    returns = models.IntegerField(default=0)
    status = models.CharField(max_length=200)
    entry_Type = models.ForeignKey(Entry_Type,on_delete=models.CASCADE)
    ledger = models.ForeignKey(Ledger,on_delete=models.CASCADE)

class Entry_Item(models.Model):
    trancsaction_type = (
        ('D', 'Debit'),
        ('C', 'Credit')
    )
    onshelf = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('F', 'Finished')
    )
    def __int__(self):
        return self.ledger 
    ledger = models.ForeignKey(Ledger,on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    pack = models.IntegerField(default=0)
    tablet = models.IntegerField(default=0)
    batch_no = models.CharField(max_length=200)
    c_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    discount_per = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    expiry = models.DateField(null=True, blank=True)
    dc = models.CharField(max_length=1, choices=trancsaction_type,default='D')
    narration = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    active_product = models.CharField(max_length=1, choices=onshelf,default='I')
    sale_price = models.IntegerField(default=0,null=True,blank=True)
    tpacks = models.IntegerField(default=0)
    rpack = models.IntegerField(default=0)
    rtablet = models.IntegerField(default=0)

class Common(models.Model):
    def __str__(self):
        return self.name 
    name = models.CharField(max_length=200)
    ledger = models.OneToOneField(Ledger,on_delete=models.CASCADE)