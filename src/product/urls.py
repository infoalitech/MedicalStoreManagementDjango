from django.urls import path
from product import views

app_name='product'

urlpatterns = [
	path('', views.index, name='index'),
	path('stock', views.stock, name='stock'),
	path('expiry', views.expiry, name='expiry'),
	path('expiry/<id>', views.expiryclear, name='expiryclear'),
	# path('expiry/return/', views.expiryreturn, name='expiryreturn'),
	path('index', views.index, name='index'),
	path('create/', views.create, name='create'),
	path('store/', views.store, name='store'),
	path('<id>', views.show, name='show'),
	path('<id>/edit/', views.edit, name='edit'),
	path('<id>/active/', views.active, name='active'),
	path('<id>/inactive/', views.inactive, name='inactive'),
	path('<id>/update/', views.update, name='update'),
	path('<id>/delete/', views.delete, name='delete')
]