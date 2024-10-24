from django.shortcuts import render, redirect, get_object_or_404
from .forms import add_outgoing_form
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import mimetypes
from django.apps import apps
import os
from django.views.decorators.csrf import csrf_exempt
from .models import Incoming, Outgoing, Internal, Decree


#index+outgoing_index functions.


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

def outgoing_mail(request):
    documents = Outgoing.objects.all()  # Use the correct model name here
    return render(request, 'outgoing_mail.html', {'documents': documents})


#add+edit+delete functions.


def add_outgoing(request):
    if request.method == 'POST':
        form = add_outgoing_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('outgoing_mail')  # Redirect back to the same form
    else:
        form = add_outgoing_form()
    
    return render(request, 'add_outgoing.html', {'form': form})


def edit_outgoing(request, outgoing_id):
    # Retrieve the specific Outgoing instance
    outgoing_document = get_object_or_404(Outgoing, id=outgoing_id)

    if request.method == 'POST':
        form = add_outgoing_form(request.POST, request.FILES, instance=outgoing_document)
        if form.is_valid():
            form.save()  # Save the updated data to the database
            return redirect('outgoing_mail')  # Redirect to the outgoing mail view
    else:
        form = add_outgoing_form(instance=outgoing_document)  # Populate the form with existing data
    
    # Use the same template for adding and editing
    return render(request, 'add_outgoing.html', {'form': form})


def delete_document(request, model_name, document_id):
    if request.method == 'DELETE':
        try:
            # Dynamically get the model class
            model = apps.get_model('documents', model_name)
            document = model.objects.get(id=document_id)
            document.delete()
            return JsonResponse({'success': True})
        except model.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Document not found'}, status=404)
        except LookupError:
            return JsonResponse({'success': False, 'error': 'Model not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


#download pdf functions.


def get_model_prefix(model_name):
    prefixes = {
        'outgoing': 'pdf_outgoing',
        'incoming': 'pdf_incoming',
        'internal': 'pdf_internal',
        'decree': 'pdf_decree',
    }
    return prefixes.get(model_name.lower(), '')

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

        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{obj.pdf_file.name}"'

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

