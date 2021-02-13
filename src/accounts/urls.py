from django.urls import path
from accounts import views

app_name='accounts'

urlpatterns = [
	path('', views.index, name='index'),
	path('cashreceive', views.cashreceive, name='receive'),
	path('cashreceive/store/', views.cashreceivestore, name='receive_store'),
	path('cashpayment', views.cashpayment, name='payment'),
	path('cashpayment/store/', views.cashpaymentstore, name='payment_store'),
	path('salary', views.salary, name='salary'),
	path('salary/store/', views.salarystore, name='salary_store'),
	path('common/', views.common, name='common'),
	path('common/<id>', views.commonshow, name='common.show')
]