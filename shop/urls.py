from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="shop"),
    path('register/', views.register, name="register"),
    path('login/', views.hlogin, name="login"),
    path('logout/', views.hlogout, name="logout"),
    path('about/', views.about, name="about"),
    path('tracker/', views.tracker, name="tracker"),
    path('contact/', views.contact, name="contact"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('forgotpass/', views.forgotpass, name='forgotpass')
]
