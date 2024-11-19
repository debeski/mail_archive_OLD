from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main index page
    path('incoming/', views.Incoming, name='incoming'),
    path('outgoing/', views.Outgoing, name='outgoing'),
    path('internal/', views.Internal, name='internal'),
    path('decrees/', views.Decree, name='decrees'),

    # Incoming_Mail URLs
    # path('add_incoming/', views.add_incoming, name='add_incoming'),
    path('incoming_mail/', views.incoming_mail, name='incoming_mail'),
    # path('edit_incoming/<int:incoming_id>/', views.edit_incoming, name='edit_incoming'),

    # Outgoing_Mail URLs:
    # path('add_outgoing/', views.add_outgoing, name='add_outgoing'),
    path('outgoing_mail/', views.outgoing_mail, name='outgoing_mail'),
    # path('edit_outgoing/<int:outgoing_id>/', views.edit_outgoing, name='edit_outgoing'),
    path('internal_mail/', views.internal_mail, name='internal_mail'),
    path('decree_mail/', views.decree_mail, name='decree_mail'),

    # 
    path('manage-sections/', views.manage_sections, name='manage_sections'),


    # Shared Urls:
    path('get_document_details/<int:document_id>/', views.get_document_details, name='get_document_details'),
    path('add/<str:model_name>/', views.add_document, name='add_document'),
    path('edit/<str:model_name>/<int:document_id>/', views.add_document, name='edit_document'),
    # path('edit/<str:model_name>/<int:document_id>/', views.edit_document, name='edit_document'),
    path('download/<str:model_name>/<int:object_id>/', views.download_document, name='download_document'),
    path('delete_document/<str:model_name>/<int:document_id>/', views.delete_document, name='delete_document'),
]