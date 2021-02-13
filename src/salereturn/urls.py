from django.urls import path
from salereturn import views

app_name='salereturn'

urlpatterns = [
	path('', views.index, name='index'),
	path('index', views.index, name='index')
]