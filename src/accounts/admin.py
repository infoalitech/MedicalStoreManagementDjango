from django.contrib import admin
from .models import Group, Ledger_Type, Ledger, Entry_Type, Entry, Entry_Item,Common
# Register your models here.


admin.site.register(Group)
admin.site.register(Ledger)
admin.site.register(Ledger_Type)
admin.site.register(Entry)
admin.site.register(Entry_Item)
admin.site.register(Entry_Type)
admin.site.register(Common)