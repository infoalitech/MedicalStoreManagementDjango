from django.urls import path
from bank import views

app_name='bank'

urlpatterns = [
	path('', views.index, name='index'),
	path('index', views.index, name='index'),
	path('create/', views.create, name='create'),
	path('store/', views.store, name='store'),
	path('<id>', views.show, name='show'),
	path('<id>/edit/', views.edit, name='edit'),
	path('<id>/update/', views.update, name='update'),
	path('<id>/delete/', views.delete, name='delete'),
	path('deposit/', views.deposit, name='deposit'),
	path('deposit/store/', views.depositstore, name='deposit_store'),
	path('withdraw/', views.withdraw, name='withdraw'),
	path('withdraw/store/', views.withdrawstore, name='withdraw_store'),
]