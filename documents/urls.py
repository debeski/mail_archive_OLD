from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    path('incoming/', views.Incoming, name='incoming'),
    path('outgoing/', views.Outgoing, name='outgoing'),
    path('internal/', views.Internal, name='internal'),
    path('decrees/', views.Decree, name='decrees'),
    path('add_outgoing/', views.add_outgoing, name='add_outgoing'),
    # path('add_incoming/', views.add_incoming, name='add_incoming'),
    # etc.
]