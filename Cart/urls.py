
from django.urls import path,include
from .views import *
urlpatterns = [

    path('',cart_summary,name='cart_summary'),
    path('delete/',cart_delete,name='cart_delete'),
    path('add/',cart_add,name='cart_add'),
    path('update/',cart_update,name='cart_update'),
]
