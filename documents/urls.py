from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    # Add more paths for other sections as needed
    path('incoming/', views.Incoming, name='incoming'),
    path('outgoing/', views.Outgoing, name='outgoing'),
    path('internal/', views.Internal, name='internal'),
    path('decrees/', views.Decree, name='decrees'),
    # path('add_incoming/', views.add_incoming, name='add_incoming'),
    # etc.
]