from django.contrib import admin
from .models import Product
from .models import Product_Types
# Register your models here.


admin.site.register(Product)
admin.site.register(Product_Types)