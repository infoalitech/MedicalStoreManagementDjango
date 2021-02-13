from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from accounts.models import Ledger, Entry, Entry_Item, Common
from product.models import Product
from supplier.models import Supplier
from customer.models import Customer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.


@login_required
def ledgerentryitems(request,id):
	ledger=Ledger.objects.get(pk=id)
	entry_items=Entry_Item.objects.all().filter(ledger=ledger)[0:20]

	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entry_items=Entry_Item.objects.filter(ledger=ledger).filter(entry__date__gte=request.POST.get('s_date'),entry__date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entry_items=Entry_Item.objects.filter(ledger=ledger).filter(entry__date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entry_items=Entry_Item.objects.filter(ledger=ledger).filter(entry__date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entry_items=Entry_Item.objects.filter(ledger=ledger).order_by('-id')



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
	context={
		'ledger':ledger,
		'entry_items':entry_items,
		'balance':balance,
		'balance_db':balance_type
	}
	return render(request,'report/ledgers.html',context)

@login_required
def index(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.all().order_by('-id')

	context={
		'entries':entries,
		'heading':"All Entries"

	}
	return render(request,'report/index.html',context)

@login_required
def sale(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='sale').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='sale').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='sale').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='sale')
	context={
		'entries':entries,
		'heading':"Sale Entries"

	}
	return render(request,'report/index.html',context)

@login_required
def salereturn(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='sale').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='sale').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='sale').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='sale')
	context={
		'entries':entries,

	}
	return render(request,'report/index.html',context)

@login_required
def purchase(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='purchase').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='purchase').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='purchase').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='purchase')
	context={
		'entries':entries,
		'heading':"Purchase Entries"

	}
	return render(request,'report/index.html',context)

@login_required
def purchasereturn(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='purchase').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='purchase').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='purchase').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='purchase')

	context={
		'entries':entries,

	}
	return render(request,'report/index.html',context)

@login_required
def cashpayment(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='cash payment').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='cash payment').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='cash payment').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='cash payment')
	context={
		'entries':entries,
		'heading':"Cash Payments"

	}
	return render(request,'report/index.html',context)

@login_required	
def cashreceive(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='cash receipt').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='cash receipt').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='cash receipt').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='cash receipt')
	context={
		'entries':entries,
		'heading':"Cash Receipts"

	}
	return render(request,'report/index.html',context)

@login_required	
def productused(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='used').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='used').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='used').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='used')
	context={
		'entries':entries,
		'heading':"Used Products"

	}
	return render(request,'report/index.html',context)

@login_required	
def bankdeposit(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='bank deposit').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='bank deposit').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='bank deposit').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='bank deposit')
	context={
		'entries':entries,
		'heading':"Bank Deposits"

	}
	return render(request,'report/index.html',context)

@login_required	
def bankwithdraw(request):
	if request.POST.get('s_date') and  request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='bank withdraw').filter(date__gte=request.POST.get('s_date'),date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('e_date'):
		entries=Entry.objects.filter(entry_Type__name='bank withdraw').filter(date__lte=request.POST.get('e_date')).order_by('-id')
	elif request.POST.get('s_date'):
		entries=Entry.objects.filter(entry_Type__name='bank withdraw').filter(date__gte=request.POST.get('s_date')).order_by('-id')
	else:
		entries=Entry.objects.filter(entry_Type__name='bank withdraw')
	context={
		'entries':entries,
		'heading':"Bank Withdraws"

	}
	return render(request,'report/index.html',context)
