from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index.html', views.index, name='index_html'),
    path('time', views.time_view, name='index'),
    path('sum', views.sum_view, name='sum'),
    path('new', views.new, name='new'),
    path('createUser', views.createUser, name='createUser'),
    path('logout', views.logout_view, name='logout'),
]
