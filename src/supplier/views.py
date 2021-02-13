from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Supplier
from accounts.models import Ledger, Ledger_Type, Group, Entry, Entry_Item,Entry_Type
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	all_suppliers=Supplier.objects.all()
	context = {
		'suppliers' : all_suppliers,
	}
	return render(request,'supplier/index.html',context)

@login_required
def create(request):
	return render(request,'supplier/create.html')

@login_required
def store(request):
	led=Ledger(balance=0,balance_dc='D'
		,group=Group.objects.get(name='liablity'),
		Ledger_Type=Ledger_Type.objects.get(name='supplier')
		)
	led.save()
	supplier=Supplier(name=request.POST['name'],
		addresss=request.POST['address'],
		phone=request.POST['phone'],
		cell=request.POST['cell'],
		email=request.POST['email'],
		initial_balance=request.POST['initial_balance'],
		initial_balance_db=request.POST['initial_balance_db'],
		ledger=led).save()	
	# initial balance entry making
	if request.POST.get('initial_balance'):
		invoice=Entry.objects.create(invoice_code='invoice',
			dr_total=int(request.POST.get('initial_balance')),
			cr_total=int(request.POST.get('initial_balance')),
			entry_Type=Entry_Type.objects.get(name='initial'),
			ledger=led,
			);
		invoice.save();
		invoice.invoice_code='INV'+str(invoice.id);
		invoice.save();
		Entry_Item.objects.create(entry=Entry.objects.get(id=invoice.id),
				ledger=led,
				total_amount=int(request.POST['initial_balance']),
				dc=request.POST['initial_balance_db'],
				).save();
	return redirect('supplier:index')

@login_required
def show(request,id):
	supplier=get_object_or_404(Supplier,pk=id)
	return render(request,'supplier/show.html',{'supplier':supplier})


@login_required
def edit(request,id):
	supplier=get_object_or_404(Supplier,pk=id)
	entry_items=Entry_Item.objects.all().filter(ledger=supplier.ledger)
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
		'supplier' : supplier,
		'balance':balance,
		'balance_db':balance_type
	}
	return render(request,'supplier/edit.html',context)

@login_required
def update(request,id):
	supplier=Supplier.objects.filter(pk=id).update(name=request.POST['name'],
		addresss=request.POST['address'],
		phone=request.POST['phone'],
		cell=request.POST['cell'],
		email=request.POST['email'],
		initial_balance=request.POST['initial_balance'],
		initial_balance_db=request.POST['initial_balance_db']
		)
	return redirect('supplier:index')

@login_required
def delete(request,id):
	supplier=get_object_or_404(Supplier,pk=id)
	supplier.delete();
	return redirect('supplier:index')
	
