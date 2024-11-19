from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddOutgoingForm, AddIncomingForm, AddInternalForm, AddDecreeForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import mimetypes
from django.apps import apps
from .models import Incoming, Outgoing, Internal, Decree
from django.core.paginator import Paginator
import logging
from django.utils import timezone
from .models import Department, Affiliate, Minister, Government
from .forms import DepartmentForm, AffiliateForm, MinisterForm, GovernmentForm


logger = logging.getLogger('myapp')  # Adjust to your app's name

def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)


def manage_sections(request):
    departments = Department.objects.all()
    affiliates = Affiliate.objects.all()
    ministers = Minister.objects.all()
    governments = Government.objects.all()

    if request.method == 'POST':
        if 'department' in request.POST:
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_sections')
        elif 'affiliate' in request.POST:
            form = AffiliateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_sections')
        elif 'minister' in request.POST:
            form = MinisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_sections')
        elif 'government' in request.POST:
            form = GovernmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_sections')

    return render(request, 'manage_sections.html', {
        'departments': departments,
        'affiliates': affiliates,
        'ministers': ministers,
        'governments': governments,
        'department_form': DepartmentForm(),
        'affiliate_form': AffiliateForm(),
        'minister_form': MinisterForm(),
        'government_form': GovernmentForm(),
    })



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



# Outgoing Mail Functions:
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
        form = AddOutgoingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('outgoing_mail')  # Redirect back to the outgoing mail view
    else:
        form = AddOutgoingForm()
    
    return render(request, 'add_outgoing.html', {'form': form})  # Use the new form template

    

# def edit_outgoing(request, outgoing_id):
#     outgoing_document = get_object_or_404(Outgoing, id=outgoing_id)

#     if request.method == 'POST':
#         form = AddOutgoingForm(request.POST, request.FILES, instance=outgoing_document)
#         if form.is_valid():
#             new_reg_number = form.cleaned_data['reg_number']
#             new_out_date = form.cleaned_data['out_date']

#             old_reg_number = outgoing_document.reg_number
#             old_out_date = outgoing_document.out_date
            
#             form.save()  # Save the form data first

#             if old_reg_number != new_reg_number or old_out_date != new_out_date:
#                 # If renaming logic is removed, you can still log changes if needed
#                 logger.info(f"Document {outgoing_id} updated: {old_reg_number} -> {new_reg_number}, {old_out_date} -> {new_out_date}")

#             return redirect('outgoing_mail')  # Redirect to the outgoing mail view
#         else:
#             logger.error(f"Form errors: {form.errors}")
#     else:
#         form = AddOutgoingForm(instance=outgoing_document)

#     return render(request, 'add_outgoing.html', {'form': form})



# Incoming Mail Functions:
def incoming_mail(request):
    documents = Incoming.objects.order_by('-id')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'incoming_mail.html', {
        'documents': page_obj,
        'show_add_and_search': True,  # Show both the add button and search field
        'page_name': 'incoming_mail',  # Set page_name for this view
    })

def add_incoming(request):
    if request.method == 'POST':
        form = AddIncomingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('incoming_mail')  # Redirect back to the incoming mail view
    else:
        form = AddIncomingForm()
    
    return render(request, 'add_incoming.html', {'form': form})  # Use the new form template


# def edit_incoming(request, incoming_id):
#     incoming_document = get_object_or_404(Incoming, id=incoming_id)

#     if request.method == 'POST':
#         form = AddIncomingForm(request.POST, request.FILES, instance=incoming_document)
#         if form.is_valid():
#             form.save()  # Save the form data first
#             return redirect('incoming_mail')  # Redirect to the incoming mail view
#         else:
#             logger.error(f"Form errors: {form.errors}")
#     else:
#         form = AddIncomingForm(instance=incoming_document)

#     return render(request, 'add_incoming.html', {'form': form})



#Shared Functions:
def edit_document(request, model_name, document_id):
    model_mapping = {
        'incoming': Incoming,
        'outgoing': Outgoing,
        'internal': Internal,
        'decree': Decree,
    }

    model = model_mapping.get(model_name.lower())
    if model is None:
        return HttpResponseNotFound('Invalid model name')

    document = get_object_or_404(model, id=document_id)

    # Determine the form to use based on the model
    form_mapping = {
        Incoming: AddIncomingForm,
        Outgoing: AddOutgoingForm,
        Internal: AddInternalForm,
        Decree: AddDecreeForm,
    }

    FormClass = form_mapping.get(type(document))
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()  # Save the form data first
            logger.info(f"Document {document_id} updated successfully.")
            return redirect(f'{model_name}_mail')  # Redirect based on model
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = FormClass(instance=document)

    return render(request, f'add_{model_name}.html', {'form': form})



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


def get_document_details(request, model_type, document_id):
    model_mapping = {
        'outgoing': Outgoing,
        'incoming': Incoming,
        'internal': Internal,
        'decree': Decree,
    }

    DocumentModel = model_mapping.get(model_type)
    if DocumentModel is None:
        return JsonResponse({'error': 'Invalid model type'}, status=400)

    document = get_object_or_404(DocumentModel, id=document_id)

    # Prepare the response data based on the model type
    data = {
        'id': document.id,
        'number': document.number,
        'date': document.date.strftime('%Y-%m-%d') if document.date else None,
        'title': document.title,
        'keywords': document.keywords,
        'pdf_file': document.pdf_file.url if document.pdf_file else None,
    }

    # Add specific fields based on the model
    if isinstance(document, Incoming):
        data.update({
            'orig_number': document.orig_number,
            'orig_date': document.orig_date.strftime('%Y-%m-%d') if document.orig_date else None,
            'dept_from': document.dept_from.name,
            'dept_to': document.dept_to.name,
        })
    elif isinstance(document, Outgoing):
        data.update({
            'dept_from': document.dept_from.name,
            'dept_to': document.dept_to.name,
        })
    elif isinstance(document, Internal):
        data.update({
            'dept_from': document.dept_from.name,
            'dept_to': document.dept_to.name,
        })
    elif isinstance(document, Decree):
        data.update({
            'minister': document.minister.name,
            'government': document.government.name,
            'attach_file': document.attach.url if document.attach else None,
        })

    return JsonResponse(data)


#download functions.
def download_document(request, model_name, object_id):
    model_mapping = {
        'outgoing': Outgoing,
        'incoming': Incoming,
        'internal': Internal,
        'decree': Decree,
    }

    model = model_mapping.get(model_name.lower())
    if model is None:
        return HttpResponseNotFound('Invalid model name')

    document = get_object_or_404(model, pk=object_id)

    # Determine the naming components
    date_str = document.date.strftime('%Y-%m-%d') if hasattr(document, 'date') and document.date else 'unknown_date'
    identifier = document.number if hasattr(document, 'number') else 'unknown'

    # Check for PDF download
    if hasattr(document, 'pdf_file') and document.pdf_file:
        content_type, _ = mimetypes.guess_type(document.pdf_file.name)
        if content_type is None:
            content_type = 'application/pdf'  # Default to PDF if unknown

        filename = f"{model_name}_pdf_{identifier}_{date_str}.pdf"
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with document.pdf_file.open('rb') as pdf_file:
            response.write(pdf_file.read())

        return response

    # Check for attachment download
    elif hasattr(document, 'attach') and document.attach:
        content_type, _ = mimetypes.guess_type(document.attach.name)
        if content_type is None:
            content_type = 'application/octet-stream'  # Default to binary if unknown

        filename = f"{model_name}_attach_{identifier}_{date_str}.{document.attach.name.split('.')[-1]}"
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with document.attach.open('rb') as attach_file:
            response.write(attach_file.read())

        return response

    else:
        return HttpResponseNotFound('Document or attachment not found')