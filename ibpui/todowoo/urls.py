"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    path('', views.home, name='home'),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('delete/<list_id>', views.delete, name='delete'),#passing in the list id primary key
    path('cross_off/<list_id>', views.cross_off, name='cross_off'),
    path('uncross/<list_id>', views.uncross, name='uncross'),
	path('edit/<list_id>', views.edit, name='edit'),
    path('addClient', views.addClient, name='addClient'),
    path('viewRequest/<list_id>', views.viewRequest, name='viewRequest'),
    path('selectAccount', views.selectAccount, name='selectAccount'),
    path('addCashMovementRequest/<list_id>', views.addCashMovementRequest, name='addCashMovementRequest'),
    path('deleteRequest/<list_id>', views.deleteRequest, name='deleteRequest'),
    path('complete/<list_id>', views.complete, name='complete'),
    path('editRequest/<list_id>', views.editRequest, name='editRequest'),
    path('viewAccount/<list_id>', views.viewAccount, name='viewAccount'),
    path('home/sendEmail', views.sendEmail, name='sendEmail'),
    path('activityLog', views.activityLog, name='activityLog'),
    path('activityLog/<month_id>', views.activityLogMonth, name='activityLogMonth'),
    path('home/<order>', views.orderBy, name='orderBy'),
    path('selectAccount/<order>', views.orderBySelect, name='orderBySelect'),
    path('change-password/', views.changePassword, name='changePassword'),
]
