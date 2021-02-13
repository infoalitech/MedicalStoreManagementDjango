from django.urls import path
from sale import views

app_name='sale'

urlpatterns = [
	path('', views.index, name='index'),
	path('getproducttype/', views.getproducttype, name='getproducttype'),
	path('getproductprice/', views.getproductprice, name='getproductprice'),
	path('getproductname/', views.getproductname, name='getproductname'),
	path('getproducttabs/', views.getproducttabs, name='getproducttabs'),
	path('salestore/', views.sale, name='sale'),
]