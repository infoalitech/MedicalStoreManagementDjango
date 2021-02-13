from django.urls import path
from dashboard import views

app_name='dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('detail/<id>/', views.entrydetail, name='detail'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='login'),
    path('register/', views.login, name='register'),
    path('setting/', views.setting, name='setting'),
    path('setting/saveexpiry', views.saveexpiry, name='saveexpiry'),
    path('setting/saveminimum', views.saveminimum, name='saveminimum'),
]
