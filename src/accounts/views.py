from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Common, Ledger, Entry, Entry_Item, Entry_Type
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
	
	return render(request,'account/index.html')

@login_required
def cashreceive(request):
	customers=Ledger.objects.filter(Ledger_Type__name='customer')
	suppliers=Ledger.objects.filter(Ledger_Type__name='supplier')
	employees=Ledger.objects.filter(Ledger_Type__name='employee')
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='cash receipt')).order_by('-id')
	context={
		'entries' : entries,
		'customers':customers,
		'suppliers':suppliers,
		'employees':employees
	}
	return render(request,'cash/receive/index.html',context)

@login_required
def cashpayment(request):
	customers=Ledger.objects.filter(Ledger_Type__name='customer')
	suppliers=Ledger.objects.filter(Ledger_Type__name='supplier')
	employees=Ledger.objects.filter(Ledger_Type__name='employee')
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='cash payment')).order_by('-id')
	context={
		'entries' : entries,
		'customers':customers,
		'suppliers':suppliers,
		'employees':employees
	}
	# return HttpResponse(suppliers)
	return render(request,'cash/payment/index.html',context)

@login_required
def cashreceivestore(request):
	ledger=int(request.POST.get('ledger'))
	amount=int(request.POST.get('amount'))
	ledger=Ledger.objects.get(pk=ledger)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='cash receipt'),
		ledger=ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();
	# Ledger entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
	ledger=ledger,
	total_amount=amount,
	dc ='C',
	).save();
	# cash entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=1),
		total_amount=amount,
		dc ='D',
		).save();	
	return redirect('accounts:receive')

@login_required
def cashpaymentstore(request):
	ledger=int(request.POST.get('ledger'))
	amount=int(request.POST.get('amount'))
	ledger=Ledger.objects.get(pk=ledger)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='cash payment'),
		ledger=ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();
	# Ledger entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
	ledger=ledger,
	total_amount=amount,
	dc ='D',
	).save();
	# cash entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=1),
		total_amount=amount,
		dc ='C',
		).save();	
	return redirect('accounts:payment')

@login_required
def common(request):
	all_common=Common.objects.all()
	context = {
		'commons' : all_common,
	}
	return render(request,'common/index.html',context)

@login_required
def commonshow(request, id):
	common=Common.objects.get(pk=id)
	entry_items=Entry_Item.objects.all().filter(ledger=common.ledger)
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
		'common' : common,
		'balance':balance,
		'balance_db':balance_type
	}
	return render(request,'common/show.html',context)




@login_required
def salary(request):
	employees=Ledger.objects.filter(Ledger_Type__name='employee')
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='pay_salary')).order_by('-id')
	context={
		'entries' : entries,
		'employees':employees
	}
	return render(request,'salary/index.html',context)

@login_required
def salarystore(request):
	ledger=int(request.POST.get('ledger'))
	amount=int(request.POST.get('amount'))
	ledger=Ledger.objects.get(pk=ledger)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='pay_salary'),
		ledger=ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();
	# Ledger entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
	ledger=ledger,
	total_amount=amount,
	dc ='D',
	).save();
	# cash entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=1),
		total_amount=amount,
		dc ='C',
		).save();	
	return redirect('accounts:salary')
