from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from accounts.models import Ledger, Entry, Entry_Item, Common
from product.models import Product
from supplier.models import Supplier
from customer.models import Customer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
	
	return HttpResponse("purchase return index")
