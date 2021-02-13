from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from accounts.models import Ledger, Entry, Entry_Item, Common, Entry_Type
from product.models import Product
from supplier.models import Supplier
from customer.models import Customer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='used')).order_by('-id')
	all_products=Product.objects.all()
	context = {
		'products' : all_products,
		'entries' : entries,
	}
	return render(request,'productused/index.html',context)


@login_required
def store(request):
	product=int(request.POST.get('product'))
	tablet=0
	packet=0
	if request.POST.get('tablet'):
		tablet=int(request.POST.get('tablet'))
	if request.POST.get('tablet'):
		packet=int(request.POST.get('packet'))
	amount=int(request.POST.get('amount'))
	productt=Product.objects.get(pk=product)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='used'),
		ledger=productt.ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();

	# Product entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=productt.ledger,
		total_amount=amount,
		tablet=tablet,
		pack=packet,
		dc ='C',
		).save();	
	# ledger entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=9),
		total_amount=amount,
		dc ='D',
		).save();

	return redirect('productused:index')	
