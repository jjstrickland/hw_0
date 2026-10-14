from django.urls import path
from . import views

urlpatterns = [
    path('time', views.time_view, name='index'),
    path('sum', views.sum_view, name='sum')
]
