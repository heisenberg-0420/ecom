from django.urls import path
from . import views

urlpatterns = [
  path('', views.store, name='store'),
  path('login/', views.login_page, name='login'),
  path('login_view/', views.login_view, name='login_view'),
  path('logout/', views.logout_view, name='logout'),
  path('register/', views.register, name='register'),
  path('cart/', views.cart, name='cart'),
  path('checkout/', views.checkout, name='checkout'),
  path('update_item/', views.update_item, name='update'),
  path('process_order/', views.process_order, name='process_order'),
]
