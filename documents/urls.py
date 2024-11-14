from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    path('incoming/', views.Incoming, name='incoming'),
    path('outgoing/', views.Outgoing, name='outgoing'),
    path('internal/', views.Internal, name='internal'),
    path('decrees/', views.Decree, name='decrees'),

    # Outgoing URLs
    path('add_outgoing/', views.add_outgoing, name='add_outgoing'),
    path('outgoing_mail/', views.outgoing_mail, name='outgoing_mail'),
    path('edit_outgoing/<int:outgoing_id>/', views.edit_outgoing, name='edit_outgoing'),

    path('get_document_details/<int:document_id>/', views.get_document_details, name='get_document_details'),
    
    # PDF/attachment download URLs + Delete URLs
    path('pdfs/<str:model_name>/<int:object_id>/', views.download_pdf, name='download_pdf'),
    path('attach/<str:model_name>/<int:object_id>/', views.download_attach, name='download_attach'),
    path('delete_document/<str:model_name>/<int:document_id>/', views.delete_document, name='delete_document'),
]