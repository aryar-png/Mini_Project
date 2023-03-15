"""Milans URL Configuration

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
from django.urls import path
from MilansApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.CommonHome,name='CommonHome'),
    path('AdminHome/',views.AdminHome,name='Admin Home'),
    path('CustomerHome/',views.CustomerHome,name='Customer Home'),
    path('CustomerSignUp/',views.CustomerSignUp,name='CustomerSignUp'),
    path('SellerSignUp/',views.SellerSignUp,name='SellerSignUp'),
    path('SignIn/',views.SignIn,name='Sign In'),
    path('changepassword/',views.changepassword,name='changepassword'),
     path('custdeactivate/',views.custdeactivate,name='custdeactivate'),
    
path('SellerHome/',views.SellerHome,name='SellerHome'),
path('SellerAddProduct/',views.SellerAddProduct,name='SellerAddProduct'),
path('SellerViewCustomers/',views.SellerViewCustomers,name='SellerViewCustomers'),
path('SellerViewProduct/',views.SellerViewProduct,name='SellerViewProduct'),
path('SellerDeleteProduct/',views.SellerDeleteProduct,name='SellerDeleteProduct'),
path('SellerUpdateProduct/',views.SellerUpdateProduct,name='SellerUpdateProduct'),
path('SellerRestoreProduct/',views.SellerRestoreProduct,name='SellerRestoreProduct'), 
path('Acceptorder/',views.Acceptorder,name='Acceptorder'), 

    path('AdminViewMyBooking/',views.AdminViewMyBooking,name='AdminViewMyBooking'),
    path('AdminViewCustomers/',views.AdminViewCustomers,name='Admin View Customers'),
    path('AdminAddCategory/',views.AdminAddCategory,name='Admin Add Category'),
    path('AdminAddSubCategory/',views.AdminAddSubCategory,name='AdminAddSubCategory'),
    path('AdminAddEvents/',views.AdminAddEvents,name='AdminAddEvents'),
    path('AdminViewFeedback/',views.AdminViewFeedback,name='Admin View Feedback'),
    path('AdminViewProduct/',views.AdminViewProduct,name='AdminViewProduct'),
    path('AdminUpdateProduct/',views.AdminUpdateProduct,name='AdminUpdateProduct'),
    path('AdminAddProduct/',views.AdminAddProduct,name='AdminAddProduct'),
    path('subcat/',views.subcat,name='subcat'),
    path('custactivate/',views.custactivate,name='custactivate'),
    path('AdminRestoreProduct/',views.AdminRestoreProduct,name='AdminRestoreProduct'), 
    path('AdminAddEventProduct/',views.AdminAddEventProduct,name='AdminAddEventProduct'), 
    path('AdminViewSeller/',views.AdminViewSeller,name='AdminViewSeller'),
    path('AdminViewsales/',views.AdminViewsales,name="AdminViewsales"),
    path('Adminactiveseller/',views.Adminactiveseller,name="Adminactiveseller"),
    path('Admindeleteseller/',views.Admindeleteseller,name="Admindeleteseller"),
    path('AdminSellerReport/',views.AdminSellerReport,name='AdminSellerReport'),
     path('SellerReport/',views.SellerReport,name='SellerReport'),
    path('AdminCategoryReport/',views.AdminCategoryReport,name='AdminCategoryReport'),
    path('AdminViewProductreport/',views.AdminViewProductreport,name="AdminViewProductreport"),
    path('billingaddress/',views.billingaddress,name='billingaddress'),
    path('CustomerSalesprediction',views.CustomerSalesprediction,name="CustomerSalesprediction"),
    
    path('CustomerAddFeedback/',views.CustomerAddFeedback,name='CustomerAddFeedback'),
    path('CustomerSearchProduct/',views.CustomerSearchProduct,name='CustomerSearchProduct'),
    path('CustomerViewProCategory/',views.CustomerViewProCategory,name='CustomerViewProCategory'),
    path('CustomerViewProSubCategory/',views.CustomerViewProSubCategory,name='CustomerViewProSubCategory'),
    path('CustomerViewProductDetails/',views.CustomerViewProductDetails,name='CustomerViewProductDetails'),
    path('CustomerViewProEvents/',views.CustomerViewProEvents,name='CustomerViewProEvents'),
    path('CustomerOrderProduct/',views.CustomerOrderProduct,name="CustomerOrderProduct"),
    path('CustomerViewCart/',views.CustomerViewCart,name="CustomerViewCart"),
    path('AdminDeleteProduct/',views.AdminDeleteProduct),
    path('CustomerViewMyBooking/',views.CustomerViewMyBooking,name="CustomerViewMyBooking"),
    path('payment1',views.payment1,name='payment1'),
    path('payment2/',views.payment2,name='payment2'),
    path('payment3/',views.payment3,name='payment3'),
    path('payment4/',views.payment4,name='payment4'),
    path('payment5/',views.payment5,name='payment5'),
    path('SubRestoreProduct/',views.SubRestoreProduct,name="SubRestoreProduct"),
    path('CatRestoreProduct/',views.CatRestoreProduct ,name="CatRestoreProduct"),
    path('AdminViewprediction', views.AdminViewprediction, name='AdminViewprediction'), 

path('myprofile/',views.MyProfile ,name="MyProfile"),
path('statistics/',views.statistics,name="statistics"),
path('my_post', views.my_post, name='my_post'),
path('my_form', views.my_form, name='my_form'),

        
         
          

]
