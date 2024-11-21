from django.urls import path
from . import views

urlpatterns = [
    # Index Url
    path('', views.index, name='index'),  # Main index page
    # Setting Url
    path('manage-sections/', views.manage_sections, name='manage_sections'),
    # Unified Urls:
    path('<str:model_name>_mail/', views.document_view, name='document_view'),
    path('get_document_details/<int:document_id>/', views.get_document_details, name='get_document_details'),
    path('add/<str:model_name>/', views.add_document, name='add_document'),
    path('edit/<str:model_name>/<int:document_id>/', views.add_document, name='edit_document'),
    path('download/<str:model_name>/<int:object_id>/', views.download_document, name='download_document'),
    path('delete_document/<str:model_name>/<int:document_id>/', views.delete_document, name='delete_document'),
]