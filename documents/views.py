from django.shortcuts import render, redirect, get_object_or_404
from .forms import add_outgoing_form, add_incoming_form, add_internal_form, add_decree_form
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import mimetypes
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from .models import Incoming, Outgoing, Internal, Decree
from django.core.paginator import Paginator
from pdf2image import convert_from_path
from django.core.files.storage import default_storage, FileSystemStorage
import os
import uuid
import logging

#index+outgoing_index functions.

# Set up logging
logger = logging.getLogger(__name__)

def index(request):
    incoming = Incoming.objects.order_by('-reg_date')[:3]
    outgoing = Outgoing.objects.order_by('-out_date')[:3]
    internal = Internal.objects.order_by('-int_date')[:3]
    decrees = Decree.objects.order_by('-dec_date')[:3]
    
    return render(request, 'index.html', {
        'incoming': incoming,
        'outgoing': outgoing,
        'internal': internal,
        'decrees': decrees,
    })

# Outgoing_mail Functions:

def outgoing_mail(request):
    documents = Outgoing.objects.order_by('-id')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'outgoing_mail.html', {
        'documents': page_obj,
        'show_add_and_search': True,  # Show both the add button and search field
        'page_name': 'outgoing_mail',  # Set page_name for this view
    })


def add_outgoing(request):
    if request.method == 'POST':
        form = add_outgoing_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('outgoing_mail')  # Redirect back to the outgoing mail view
    else:
        form = add_outgoing_form()
    
    return render(request, 'add_outgoing.html', {'form': form})  # Use the new form template


def edit_outgoing(request, outgoing_id):
    outgoing_document = get_object_or_404(Outgoing, id=outgoing_id)

    if request.method == 'POST':
        form = add_outgoing_form(request.POST, request.FILES, instance=outgoing_document)
        if form.is_valid():
            new_reg_number = form.cleaned_data['reg_number']
            new_out_date = form.cleaned_data['out_date']

            old_reg_number = outgoing_document.reg_number
            old_out_date = outgoing_document.out_date
            
            form.save()  # Save the form data first

            if old_reg_number != new_reg_number or old_out_date != new_out_date:
                # If renaming logic is removed, you can still log changes if needed
                logger.info(f"Document {outgoing_id} updated: {old_reg_number} -> {new_reg_number}, {old_out_date} -> {new_out_date}")

            return redirect('outgoing_mail')  # Redirect to the outgoing mail view
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = add_outgoing_form(instance=outgoing_document)

    return render(request, 'add_outgoing.html', {'form': form})

def rename_pdf_file(document, new_reg_number, new_out_date):
    old_file_path = document.pdf_file.path
    new_pdf_name = f'{new_reg_number}_{new_out_date.strftime("%Y-%m-%d")}.pdf'
    new_file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'outgoing', new_pdf_name)

    logger.debug(f"Old file path: {old_file_path}")
    logger.debug(f"New file path: {new_file_path}")

    if os.path.exists(old_file_path):
        try:
            os.rename(old_file_path, new_file_path)
            logger.info(f"Successfully renamed '{old_file_path}' to '{new_file_path}'")
            document.pdf_file.name = f'pdfs/outgoing/{new_pdf_name}'
            document.save()  # Save the updated document name
        except Exception as e:
            logger.error(f"Error renaming file: {e}")
    else:
        logger.warning(f"Old file path does not exist: {old_file_path}")


def get_document_details(request, document_id):
    document = Outgoing.objects.get(id=document_id)

    data = {
        'id': document.id,
        'reg_number': document.reg_number,
        'out_date': document.out_date.strftime('%Y-%m-%d'),
        'dept_from': document.dept_from,
        'dept_to': document.dept_to,
        'title': document.title,
        'keywords': document.keywords,
        'pdf_file': document.pdf_file.url if document.pdf_file else None,  # Send the PDF file URL
    }
    return JsonResponse(data)
    
def delete_document(request, model_name, document_id):
    if request.method == 'DELETE':
        try:
            # Dynamically get the model class
            model = apps.get_model('documents', model_name)
            document = model.objects.get(id=document_id)
            document.delete()
            return JsonResponse({'success': True})
        except (model.DoesNotExist, LookupError):
            return JsonResponse({'success': False, 'error': 'Document or model not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


#download pdf functions.

def download_pdf(request, model_name, object_id):
    model_mapping = {
        'outgoing': Outgoing,
        'incoming': Incoming,
        'internal': Internal,
        'decree': Decree,
    }

    model = model_mapping.get(model_name.lower())
    if model is None:
        return HttpResponseNotFound('Invalid model name')

    obj = get_object_or_404(model, pk=object_id)

    # Check if the PDF file exists
    if obj.pdf_file:
        content_type, _ = mimetypes.guess_type(obj.pdf_file.name)
        if content_type is None:
            content_type = 'application/pdf'  # Default to PDF if unknown

        # Create the filename in the desired format
        date_str = obj.out_date.strftime('%Y-%m-%d') if hasattr(obj, 'out_date') else 'unknown_date'
        filename = f"{model_name}_{obj.reg_number}_{date_str}.pdf"

        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with obj.pdf_file.open('rb') as pdf_file:
            response.write(pdf_file.read())

        return response
    else:
        return HttpResponseNotFound('PDF file not found or invalid')


def download_attach(request, model_name, object_id):
    model_mapping = {
        'outgoing': Outgoing,
        'incoming': Incoming,
        'internal': Internal,
        'decree': Decree,
    }

    model = model_mapping.get(model_name.lower())
    if model is None:
        return HttpResponseNotFound('Invalid model name')

    obj = get_object_or_404(model, pk=object_id)

    # Check if the attachment exists
    if obj.attach:
        content_type, _ = mimetypes.guess_type(obj.attach.name)
        if content_type is None:
            content_type = 'application/octet-stream'  # Default to binary if unknown

        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{obj.attach.name}"'

        with obj.attach.open('rb') as attach_file:
            response.write(attach_file.read())

        return response
    else:
        return HttpResponseNotFound('Attachment file not found or invalid')
