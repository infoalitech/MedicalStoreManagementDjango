from django.urls import path
from employee import views

app_name='employee'

urlpatterns = [
	path('', views.index, name='index'),
	path('index', views.index, name='index'),
	path('create/', views.create, name='create'),
	path('store/', views.store, name='store'),
	path('<id>', views.show, name='show'),
	path('<id>/edit/', views.edit, name='edit'),
	path('<id>/update/', views.update, name='update'),
	path('<id>/delete/', views.delete, name='delete')
]