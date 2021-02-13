from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from accounts.models import Ledger, Entry, Entry_Item, Common, Entry_Type
from product.models import Product
from supplier.models import Supplier
from customer.models import Customer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
# Create your views here.

@login_required
def index(request):
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='sale')).order_by('-id')
	all_products=Product.objects.all().filter(active=0)
	customers=Customer.objects.all()
	context = {
		'products' : all_products,
		'customers' : customers,
		'entries' : entries,
	}
	return render(request,'sale/index.html',context)

@login_required
def getproducttype(request):
	product=Product.objects.get(pk=request.POST['product_id'])
	return HttpResponse(product.type_id)

@login_required
def getproductprice(request):
	product=Product.objects.get(pk=request.POST['product_id'])
	# return HttpResponse(product.name)

	entries=Entry_Item.objects.filter(entry__entry_Type=Entry_Type.objects.get(name='purchase')).filter(active_product='A').filter(ledger=product.ledger)
	
	# return HttpResponse(len(entries))
	if len(entries) > 0:
		# return HttpResponse("found active")
		return HttpResponse(entries[0].sale_price)
	else:
		entry=Entry_Item.objects.filter(entry__entry_Type=Entry_Type.objects.get(name='purchase')).filter(active_product='I').filter(ledger=product.ledger).order_by('entry__date')
		if len(entry) > 0:
			entry[0].active_product="A"
			entry[0].save()
			return HttpResponse(entry[0].sale_price)
		else:
			return HttpResponse("No Purchase Yet")



@login_required
def getproductname(request):
	product=Product.objects.get(pk=request.POST['product_id'])
	return HttpResponse(product.name)

@login_required
def getproducttabs(request):
	product=Product.objects.get(pk=request.POST['product_id'])
	return HttpResponse(product.tablets)

@login_required
def sale(request):
	# Invoice GEneration

	Ttotal=int(request.POST.get('Ttotal'))
	Tdiscount= int(request.POST.get('Tdiscount'))
	Treceivable= int(request.POST.get('Treceivable'))
	# customer=0
	if request.POST.get('customer'):
		customer=Customer.objects.get(pk=int(request.POST.get('customer')))
		entry_ledger=customer.ledger
	else:
		entry_ledger=Ledger.objects.get(pk=9)
	if request.POST.get('received'):
		received =int(request.POST.get('received'))
	remaining= 0
	if Ttotal-(Tdiscount+received):
		remaining= Ttotal-(Tdiscount+received)

	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=Ttotal,
		cr_total=Ttotal,
		remaining=remaining,
		entry_Type=Entry_Type.objects.get(name='sale'),
		ledger=entry_ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();
	# Product looping and entry making
	product=request.POST.getlist('pid[]')
	price=request.POST.getlist('ppri[]')
	packs=request.POST.getlist('ppack[]')
	tablet=request.POST.getlist('ptab[]')
	total=request.POST.getlist('ptotal[]')
	discount=request.POST.getlist('pdiscount[]')
	receivable=request.POST.getlist('preceivable[]')

	i =0
	length = len(request.POST.getlist('pid[]'))
	
	while i < length:
		prod=Product.objects.get(pk=int(product[i]))
		item=Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=prod.ledger,
		pack=packs[i],
		tablet=tablet[i],
		price=price[i],
		total_amount=int(total[i]),
		discount=int(discount[i]),
	    dc ='C',
	    narration ='prodcut sale',
		).save();	
		if  int(tablet[i]) > int(prod.tablets):
			tab = int(tablet[i]) % int(prod.tablets)
			pack =int(packs[i])+ ((int(tablet[i])-tab) /  int(prod.tablets)) 
		else:
			tab = int(tablet[i])
			pack =int(packs[i])

		prod.sale_pack=prod.sale_pack+pack
		prod.sale_tablet=prod.sale_tablet+tab

		maintainstock(request,prod.id,pack,tab)



		prod.stock_pack=prod.stock_pack-pack
		prod.stock_tablet=prod.stock_tablet-tab

		prod.save()
		i=i+1
		# return HttpResponse(item)
		# Entry_Item.save();
	# customer entry
	if request.POST.get('customer'):
		if remaining > 0:
			Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				ledger=customer.ledger,
				total_amount=remaining,
				dc ='D',
				).save();	
	# cash entry
	if request.POST.get('received'):
		if int(request.POST.get('received')) > 0:
			Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				# ledger=Ledger.objects.get(pk=int(product[i])),
				ledger=Ledger.objects.get(id=1),
				total_amount=received,
				dc ='D',
				).save();	

	# discount allowed
	if request.POST.get('Tdiscount'):
		if int(request.POST.get('Tdiscount')) > 0:
			Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				# ledger=Ledger.objects.get(pk=int(product[i])),
				ledger=Ledger.objects.get(id=3),
				total_amount=int(request.POST.get('Tdiscount')),
				dc ='D',
				).save();
	# loss account
	if request.POST.get('loss'):
		if int(request.POST.get('loss')) > 0:
			Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				ledger=Ledger.objects.get(id=8),
				total_amount=remaining,
				dc ='D',
				).save();	

	# redirect to report page
	return redirect('/sale/')


def maintainstock(request,pid,pack,tab):
	prod=Product.objects.get(pk=pid)
	entry=Entry_Item.objects.filter(entry__entry_Type=Entry_Type.objects.get(name='purchase')).filter(active_product='A').filter(ledger=prod.ledger)
	nextentry=False
	if len(entry) > 0:
		if entry[0].rpack > pack:
			entry[0].rpack=entry[0].rpack-pack
			pack=0
			entry[0].save()
		else:
			pack=pack-entry[0].rpack
			entry[0].rpack=0
			entry[0].active_product="F"
			entry[0].save()
			nextentry=True
		if entry[0].rtablet > tab:
			entry[0].rtablet=entry[0].rtablet-tab
			tab=0
			entry[0].save()
		else:
			if entry[0].rpack > 0:
				entry[0].rpack-1
				entry[0].rtablet=prod.tablets
				entry[0].rtablet=int(entry[0].rtablet)-int(tab)
				tab=0
				entry[0].save()
			else:
				nextentry=True
		if nextentry== True:
			entries=Entry_Item.objects.filter(entry__entry_Type=Entry_Type.objects.get(name='purchase')).filter(active_product='I').filter(ledger=prod.ledger).order_by('entry__date')
			if len(entries) > 0:
				entries[0].active_product="A"
				entries[0].save()
			else:
				print("Stock Crashed Sorry You SOld More Than Purchase")
			maintainstock(request,pid,pack,tab)
	return 0