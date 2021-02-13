from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Bank
from accounts.models import Ledger
from accounts.models import Ledger, Ledger_Type, Group, Entry, Entry_Item, Entry_Type
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	all_banks=Bank.objects.all()
	context = {
		'banks' : all_banks,
	}
	return render(request,'bank/index.html',context)

@login_required
def create(request):
	return render(request,'bank/create.html')

@login_required
def store(request):
	led=Ledger(balance=0,balance_dc='D'
		,group=Group.objects.get(name='asset'),
		Ledger_Type=Ledger_Type.objects.get(name='bank')
		)
	led.save()
	bank=Bank(name=request.POST['name'],
		branch=request.POST['branch'],
		account_title=request.POST['account_title'],
		account_no=request.POST['account_no'],
		initial_balance=request.POST['initial_balance'],
		initial_balance_db=request.POST['initial_balance_db'],
		ledger=led)
	bank.save()
	
	# initial balance entry making
	if request.POST.get('initial_balance'):
		invoice=Entry.objects.create(invoice_code='invoice',
			dr_total=int(request.POST.get('initial_balance')),
			cr_total=int(request.POST.get('initial_balance')),
			entry_Type=Entry_Type.objects.get(name='initial'),
			ledger=bank.ledger,
			);
		invoice.save();
		invoice.invoice_code='INV'+str(invoice.id);
		invoice.save();
		Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				ledger=bank.ledger,
				total_amount=int(request.POST['initial_balance']),
				dc=request.POST['initial_balance_db'],
				).save();
	return redirect('bank:index')

@login_required
def show(request,id):
	bank=get_object_or_404(Bank,pk=id)
	entry_items=Entry_Item.objects.all().filter(ledger=bank.ledger)
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
		'bank' : bank,
		'balance':balance,
		'balance_db':balance_type
	}
	return render(request,'bank/show.html',context)

@login_required
def edit(request,id):
	bank=get_object_or_404(Bank,pk=id)
	return render(request,'bank/edit.html',{'bank':bank})

@login_required
def update(request,id):
	Bank.objects.filter(pk=id).update(name=request.POST['name'],
		branch=request.POST['branch'],
		account_title=request.POST['account_title'],
		account_no=request.POST['account_no'],
		initial_balance=request.POST['initial_balance'],
		initial_balance_db=request.POST['initial_balance_db']
		)
	return redirect('bank:index')

@login_required
def delete(request,id):
	bank=get_object_or_404(Bank,pk=id)
	bank.delete();
	return redirect('bank:index')
	

@login_required
def deposit(request):
	all_banks=Bank.objects.all()
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='bank deposit')).order_by('-id')
	context = {
		'banks' : all_banks,
		'entries' : entries,
	}
	return render(request,'bank/deposit/index.html',context)

@login_required
def withdraw(request):
	all_banks=Bank.objects.all()
	entries=Entry.objects.filter(entry_Type=Entry_Type.objects.get(name='bank withdraw')).order_by('-id')
	context = {
		'banks' : all_banks,
		'entries' : entries,
	}
	return render(request,'bank/withdraw/index.html',context)
	
	

@login_required
def depositstore(request):
	amount=int(request.POST.get('amount'))
	bank=int(request.POST.get('bank'))
	bank=Bank.objects.get(pk=bank)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='bank deposit'),
		ledger=bank.ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();
	# Bank entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=bank.ledger,
		total_amount=amount,
		dc ='D',
		).save();	
	# cash entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=1),
		total_amount=amount,
		dc ='C',
		).save();	
	return redirect('bank:deposit')
	
	

@login_required
def withdrawstore(request):
	amount=int(request.POST.get('amount'))
	bank=int(request.POST.get('bank'))
	bank=Bank.objects.get(pk=bank)
	invoice=Entry.objects.create(invoice_code='invoice',
		dr_total=amount,
		cr_total=amount,
		entry_Type=Entry_Type.objects.get(name='bank withdraw'),
		ledger=bank.ledger,
		);
	invoice.save();
	invoice.invoice_code='INV'+str(invoice.id);
	invoice.save();

	# Bank entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=bank.ledger,
		total_amount=amount,
		dc ='C',
		).save();	
	# cash entry
	Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
		ledger=Ledger.objects.get(id=1),
		total_amount=amount,
		dc ='D',
		).save();	
	return redirect('bank:withdraw')	
