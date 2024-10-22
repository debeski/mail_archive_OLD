from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    # Add more paths for other sections as needed
    # path('incoming/', views.Incoming, name='incoming'),
    # path('outgoing/', views.Outgoing, name='outgoing'),
    # path('internal/', views.Internal, name='internal'),
    # path('decrees/', views.Decree_view, name='decrees'),
    path('add_decree', views.add_decree, name='add_decree'),
    # path('add_incoming/', views.add_incoming, name='add_incoming'),
    # etc.
]