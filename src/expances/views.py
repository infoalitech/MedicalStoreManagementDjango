from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Expance
from accounts.models import Entry,Entry_Item,Entry_Type,Ledger,Ledger_Type
from django.utils import timezone

from accounts.models import Ledger, Ledger_Type, Group, Entry, Entry_Item
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	all_expances=Expance.objects.all()
	context = {
		'expances' : all_expances,
	}
	return render(request,'expances/index.html',context)

@login_required
def create(request):
	return render(request,'expances/create.html')

@login_required
def store(request):
	led=Ledger(balance=0,balance_dc='D',
		group=Group.objects.get(name='expances'),
		Ledger_Type=Ledger_Type.objects.get(name='expances')
		)
	led.save()
	expance=Expance(name=request.POST['name'],
		initial_balance=request.POST['initial_balance'],
		initial_balance_db=request.POST['initial_balance_db'],
		ledger=led)
	expance.save()	
	# initial balance entry making
	if request.POST.get('initial_balance'):
		invoice=Entry.objects.create(invoice_code='invoice',
			dr_total=int(request.POST.get('initial_balance')),
			cr_total=int(request.POST.get('initial_balance')),
			entry_Type=Entry_Type.objects.get(name='initial'),
			ledger=expance.ledger,
			);
		invoice.save();
		invoice.invoice_code='INV'+str(invoice.id);
		invoice.save();
		Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				ledger=expance.ledger,
				total_amount=int(request.POST['initial_balance']),
				dc=request.POST['initial_balance_db'],
				).save();
	return redirect('expances:index')

@login_required
def show(request,id):
	expance=get_object_or_404(Expance,pk=id)
	entry_items=Entry_Item.objects.all().filter(ledger=expance.ledger)
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
		'expance' : expance,
		'balance':balance,
		'balance_db':balance_type
	}
	return render(request,'expances/show.html',context)

@login_required
def edit(request,id):
	expance=get_object_or_404(Expance,pk=id)
	return render(request,'expances/edit.html',{'expance':expance})

@login_required
def update(request,id):
	Expance.objects.filter(pk=id).update(name=request.POST['name'],
		initial_balance=request.POST['initial_balance'],
		initial_balance_db=request.POST['initial_balance_db']
		)
	return redirect('expances:index')

@login_required
def delete(request,id):
	expance=get_object_or_404(Expance,pk=id)
	expance.delete();
	return redirect('expances:index')
	

@login_required
def pay(request):
	expances=Expance.objects.all()
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='expances')).order_by('-id')
	context = {
		'expances' : expances,
		'entries' : entries,
	}
	return render(request,'expances/pay/index.html',context)

@login_required
def paystore(request):
	expance=int(request.POST.get('expance'))
	amount=int(request.POST.get('amount'))
	expance=Expance.objects.get(pk=expance)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='expances'),
		ledger=expance.ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();

	# Expance entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=expance.ledger,
		total_amount=amount,
		dc ='D',
		).save();	
	# cash entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=1),
		total_amount=amount,
		dc ='C',
		).save();	
	return redirect('expances:pay')	
