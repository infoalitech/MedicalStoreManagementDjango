from django.urls import path
from purchasereturn import views

app_name='purchasereturn'

urlpatterns = [
	path('', views.index, name='index')
]