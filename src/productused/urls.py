from django.urls import path
from productused import views

app_name='productused'

urlpatterns = [
	path('', views.index, name='index'),
	path('store/', views.store, name='store')
]