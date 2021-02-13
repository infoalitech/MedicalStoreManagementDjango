from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from accounts.models import Ledger, Entry, Entry_Item, Entry_Type, Common
from product.models import Product
from supplier.models import Supplier
from customer.models import Customer
from bank.models import Bank
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='purchase')).order_by('-id')
	all_products=Product.objects.all()
	banks=Bank.objects.all()
	suppliers=Supplier.objects.all()
	context = {
		'products' : all_products,
		'banks' : banks,
		'suppliers' : suppliers,
		'entries' : entries,
	}
	return render(request,'purchase/index.html',context)


@login_required
def getsupplier(request):
	supplier=Supplier.objects.get(pk=request.POST['supp_id'])
	return HttpResponse(supplier.initial_balance)



@login_required
def store(request):
# Supplier Fetching
	if request.POST.get('supplier'):
		supplier=Supplier.objects.get(pk=int(request.POST.get('supplier')))
# Netpayable
	prri=int(request.POST.get('prri'))
# Netpayable
	netpayable=int(request.POST.get('netpayable'))
# pre_balance
	pre_balance=int(request.POST.get('pre_balance'))
# paid
	paid=int(request.POST.get('paid'))
# tottal
	curr_payable=int(request.POST.get('tottal'))
# due
	due=int(request.POST.get('due'))
# discount
	diis=int(request.POST.get('diis'))
# sttax
	sttax=int(request.POST.get('sttax'))
# prev cleared
	supp_debit=0
	supp_credit=0
	if curr_payable < paid:
		supp_debit = paid - curr_payable
		totall = prri + supp_debit
	else:
		totall=prri

	if curr_payable > paid:
		supp_credit = due - pre_balance
# Invoice Generation
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=totall,
		cr_total=totall,
		entry_Type=Entry_Type.objects.get(name='purchase'),
		ledger=supplier.ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();
	# Product looping and entry making
	product=request.POST.getlist('product[]')
	quantity=request.POST.getlist('qty[]')
	packets=request.POST.getlist('packet[]')
	batch=request.POST.getlist('batch[]')
	c_price=request.POST.getlist('price[]')
	price=request.POST.getlist('pricetotal[]')
	discount_per=request.POST.getlist('discount[]')
	discount_amount=request.POST.getlist('discountamount[]')
	tax_amount=request.POST.getlist('s_taxamount[]')
	total=request.POST.getlist('total[]')
	expiry=request.POST.getlist('expiry[]')
	s_price=request.POST.getlist('s_price[]')

	i =0
	length = len(request.POST.getlist('product[]'))
	while i < length:
		prod=Product.objects.get(pk=int(product[i]))
		# Product Account
		item=Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=prod.ledger,
	    quantity=int(quantity[i]),
	    pack =int(quantity[i]),
	    tpacks =int(packets[i])*int(packets[i]),
	    rpack =int(quantity[i])*int(packets[i]),
	    batch_no =batch[i],
	    sale_price =s_price[i],
	    # c_price =int(c_price[i]),
	    price =int(price[i]),
	    tax =int(tax_amount[i]),
	    # discount_per =int(discount_per[i]),
	    discount =int(discount_amount[i]),
	    total_amount =( int(total[i]) + int(discount_amount[i])) ,
	    expiry =expiry[i],
	    dc ='D',
	    narration ='prodcut purchase',
	    status =0,
		).save();
		pack=int(quantity[i])*int(packets[i])
		prod.purchase_pack = prod.purchase_pack + pack
		prod.stock_pack = prod.stock_pack + pack
		prod.price = int(s_price[i])
		prod.save()
		i=i+1
	# Supplier entry
	if supp_debit:
		# in case on debit
		Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
			ledger=supplier.ledger,
			total_amount=supp_debit,
			dc ='D',
			).save();

	# discount received
	if request.POST.get('diis'):
		if int(request.POST.get('diis')) > 0:
			Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				# ledger=Ledger.objects.get(pk=int(product[i])),
				ledger=Ledger.objects.get(id=4),
				total_amount=diis,
				dc ='C',
				).save();
	if supp_credit:
		# in case of credit
		Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
			ledger=supplier.ledger,
			total_amount=supp_credit,
			dc ='C',
			).save();	

	# cash entry
	if request.POST.get('paid'):
		if int(request.POST.get('paid')) > 0:
			Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				ledger=Ledger.objects.get(id=1),
				total_amount=paid,
				dc ='C',
				).save();	

	# # Tax
	# if request.POST.get('sttax'):
	# 	if int(request.POST.get('sttax')) > 0:
	# 		Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
	# 			# ledger=Ledger.objects.get(pk=int(product[i])),
	# 			ledger=Ledger.objects.get(id=10),
	# 			total_amount=sttax,
	# 			dc ='C',
	# 			).save();

	# redirect to report page
	return redirect('/purchase/')