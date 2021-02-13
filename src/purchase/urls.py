from django.urls import path
from purchase import views

app_name='purchase'

urlpatterns = [
	path('', views.index, name='index'),
	path('getsupplier/', views.getsupplier, name='getsupplier'),
	path('purchasestore/', views.store, name='store')
]