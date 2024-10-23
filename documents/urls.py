from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    path('incoming/', views.Incoming, name='incoming'),
    path('outgoing/', views.Outgoing, name='outgoing'),
    path('internal/', views.Internal, name='internal'),
    path('decrees/', views.Decree, name='decrees'),
    path('add_outgoing/', views.add_outgoing, name='add_outgoing'),
    path('outgoing_mail/', views.outgoing_mail, name='outgoing_mail'),  # Updated URL path
    path('pdfs/outgoing/<int:outgoing_id>/', views.download_outgoing_pdf, name='download_outgoing_pdf'),
    path('edit_outgoing/<int:outgoing_id>/', views.edit_outgoing, name='edit_outgoing'),  # Keep underscores

    # path('add_incoming/', views.add_incoming, name='add_incoming'),
    # etc.
]