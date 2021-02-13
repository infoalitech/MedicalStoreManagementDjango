from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Product, Product_Types
from supplier.models import Supplier
from accounts.models import Ledger, Ledger_Type, Group, Entry, Entry_Type, Entry_Item
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	all_products=Product.objects.all()
	context = {
		'products' : all_products,
	}
	return render(request,'product/index.html',context)

@login_required
def stock(request):
	all_products=Product.objects.all().filter(active=0)
	context = {
		'products' : all_products,
	}
	return render(request,'stock/index.html',context)
	
@login_required
def expiry(request):
	# entries=Entry.objects.filter(entry_Type__name='purchase')
	entry_items=Entry_Item.objects.filter(entry__entry_Type__name='purchase').filter(ledger__Ledger_Type__name='product').filter(status=0)
	all_products=Product.objects.all() 
	context = {
		'products' : all_products,
		'purchases' : entry_items,
	}
	return render(request,'expiry/index.html',context)
	
@login_required
def expiryclear(request,id):
	Entry_Item.objects.filter(pk=id).update(status=1)
	return redirect('product:expiry')

@login_required
def create(request):

	producttypes=Product_Types.objects.all()
	suppliers=Supplier.objects.all()
	context = {
		'producttypes' 	: producttypes,
		'suppliers'	: suppliers,
	}
	return render(request,'product/create.html',context)

@login_required
def store(request):
	led=Ledger(balance=0,balance_dc='D'
		,group=Group.objects.get(name='asset'),
		Ledger_Type=Ledger_Type.objects.get(name='product')
		)
	led.save()
	product=Product(name=request.POST['name'],
		code=request.POST['code'],
		mg=request.POST['mg'],
		price=request.POST['price'],
		type_id=request.POST['type'],
		tablets=request.POST['tablets'],
		s_pack=request.POST['s_pack'],
		s_tablet=request.POST['s_tab'],
		stock_pack=request.POST['s_pack'],
		stock_tablet=request.POST['s_tab'],
		active='0',
		ledger=led)
	product.created_date=timezone.now()
	
	product.save()
	return redirect('product:index')

@login_required
def show(request,id):
	product=get_object_or_404(Product,pk=id)
	entry_items=Entry_Item.objects.all().filter(ledger=product.ledger)
	debit_balance=0;
	credit_balance=0;
	for item in entry_items:
		if item.dc == 'D':
			debit_balance=debit_balance+item.total_amount
		if item.dc == 'C':
			credit_balance=credit_balance+item.total_amount
	if debit_balance > credit_balance:
		balance_type = "Debit "	
		balance= debit_balance - credit_balance
	if debit_balance < credit_balance:
		balance_type = "Credit "
		balance= credit_balance - debit_balance	
	if debit_balance == credit_balance:
		balance_type = "None"
		balance= 0
	context = {
		'product' : product,
		'balance':balance,
		'balance_db':balance_type
	}
	return render(request,'product/show.html',context)

@login_required
def edit(request,id):
	producttypes=Product_Types.objects.all()
	product=get_object_or_404(Product,pk=id)
	suppliers=Supplier.objects.all()
	context = {
		'product':product,
		'producttypes' 	: producttypes,
		'suppliers'	: suppliers,
	}
	return render(request,'product/edit.html',context)

@login_required
def update(request,id):
	product=Product.objects.filter(pk=id).update(name=request.POST['name'],
	code=request.POST['code'],
	mg=request.POST['mg'],
	price=request.POST['price'],
	type_id=request.POST['type'],
	tablets=request.POST['tablets'],
	s_pack=request.POST['s_pack'],
	s_tablet=request.POST['s_tab'])
	return redirect('product:index')

@login_required
def delete(request,id):
	product=get_object_or_404(Product,pk=id)
	product.delete();
	return redirect('/product/')

@login_required
def active(request,id):
	product=Product.objects.filter(pk=id).update(active='0')
	return redirect('/product/')

@login_required
def inactive(request,id):
	product=Product.objects.filter(pk=id).update(active='1')
	return redirect('/product/')