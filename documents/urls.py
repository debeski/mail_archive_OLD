from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Index Url
    path('', views.index, name='index'),
    # Manage Sections Url
    path('manage/<str:model_name>/', views.manage_sections, name='manage_sections'),
    # Unified Urls:
    path('documents/<str:model_name>/', views.document_view, name='document_view'),
    path('documents/<str:model_name>/add/', views.add_document, name='add_document'),
    path('documents/<str:model_name>/edit/<int:document_id>/', views.add_document, name='edit_document'),
    path('download/<str:model_name>/<int:object_id>/', views.download_document, name='download_document'),
    path('delete_document/<str:model_name>/<int:document_id>/', views.delete_document, name='delete_document'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('clear_login_modal_flag/', views.clear_login_modal_flag, name='clear_login_modal_flag'),
    # path('get_document_details/<int:document_id>/', views.get_document_details, name='get_document_details'),
]