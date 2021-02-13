from django.urls import path
from report import views

app_name='report'

urlpatterns = [
	path('', views.index, name='index'),
	path('ledger/<id>', views.ledgerentryitems, name='Ledger'),
	path('sale', views.sale, name='salereport'),
	path('salereturn', views.salereturn, name='sale_returnreport'),
	path('purchase', views.purchase, name='purchasereport'),
	path('purchasereturn', views.purchasereturn, name='purchase_returnreport'),
	path('cashpayment', views.cashpayment, name='cashpaymentreport'),
	path('cashreceive', views.cashreceive, name='cashreceivereport'),
	path('productused', views.productused, name='productusedreport'),
	path('bankdeposit', views.bankdeposit, name='Bank-Depositreport'),
	path('bankwithdraw', views.bankwithdraw, name='Bank-withdrawreport'),
]