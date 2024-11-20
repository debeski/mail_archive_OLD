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
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np
import os
from django.conf import settings
from io import BytesIO
import zipfile



logger = logging.getLogger('myapp')  # Adjust to your app's name

def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)

from datetime import datetime

def create_charts():
    # Set font properties
    rcParams['font.family'] = 'Arial'  # Ensure you have the font installed
    rcParams['font.size'] = 12

    # Define the years you want to analyze
    years = range(2018, 2024)  # Adjust the range as necessary
    counts = {model: [] for model in ['Incoming', 'Outgoing', 'Internal', 'Decree']}

    for year in years:
        counts['Incoming'].append(Incoming.objects.filter(date__year=year).count() or 0)
        counts['Outgoing'].append(Outgoing.objects.filter(date__year=year).count() or 0)
        counts['Internal'].append(Internal.objects.filter(date__year=year).count() or 0)
        counts['Decree'].append(Decree.objects.filter(date__year=year).count() or 0)

    print("Counts per model per year:", counts)

    # Create a grouped bar chart
    fig, ax = plt.subplots()
    bar_width = 0.2
    index = np.arange(len(years))

    for i, model in enumerate(counts.keys()):
        ax.bar(index + i * bar_width, counts[model], bar_width, label=model)

    ax.set_xlabel('السنوات', labelpad=10, fontsize=14, ha='right')  # Align right
    ax.set_ylabel('عدد الوثائق', labelpad=10, fontsize=14, ha='right')  # Align right
    ax.set_title('عدد الوثائق حسب السنة', fontsize=16, ha='right')  # Align right
    ax.set_xticks(index + bar_width * 1.5)
    ax.set_xticklabels(years, ha='right')  # Align right
    ax.legend()

    # Save the grouped bar chart
    bar_chart_path = os.path.join(settings.BASE_DIR, 'documents/static/chart', 'grouped_bar_chart.png')
    plt.savefig(bar_chart_path, bbox_inches='tight')
    plt.close(fig)

    # Prepare data for the pie chart
    total_counts = [sum(counts[model]) for model in counts.keys()]
    print("Total counts for pie chart before plotting:", total_counts)

    # Check if all counts are zero
    if all(count == 0 for count in total_counts):
        print("No data available for pie chart.")
        return  # Skip pie chart creation

    # Handle NaN values
    total_counts = [0 if np.isnan(count) else count for count in total_counts]  # Ensure no NaNs

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(total_counts, labels=counts.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Set title for the pie chart
    ax.set_title('توزيع الوثائق حسب النوع', fontsize=16, ha='right')  # Align right

    # Save the pie chart
    pie_chart_path = os.path.join(settings.BASE_DIR, 'documents/static/chart', 'pie_chart.png')
    plt.savefig(pie_chart_path)
    plt.close(fig)



# Html Rendering Functions:
def index(request):
    create_charts()  # Generate charts before rendering the template

    latest_documents = (
        list(Incoming.objects.order_by('-created_at')[:5]) +
        list(Outgoing.objects.order_by('-created_at')[:5]) +
        list(Internal.objects.order_by('-created_at')[:5]) +
        list(Decree.objects.order_by('-created_at')[:5])
    )[:5]  # Combine and limit to the latest 7 documents

    return render(request, 'index.html', {
        'latest_documents': latest_documents,
    })


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


def incoming_mail(request):
    documents = Incoming.objects.order_by('-id')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'incoming_mail.html', {
        'documents': page_obj,
        'show_add_and_search': True,  # Show both the add button and search field
        'page_name': 'incoming_mail',  # Set page_name for this view
        'model_name': 'incoming'.strip(),  # Pass the model name

    })


def outgoing_mail(request):
    documents = Outgoing.objects.order_by('-id')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'outgoing_mail.html', {
        'documents': page_obj,
        'show_add_and_search': True,
        'page_name': 'outgoing_mail',
        'model_name': 'outgoing'.strip(),  # Pass the model name
    })


def internal_mail(request):
    documents = Internal.objects.order_by('-id')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'internal_mail.html', {
        'documents': page_obj,
        'show_add_and_search': True,
        'page_name': 'internal_mail',
        'model_name': 'internal'.strip(),  # Pass the model name
    })


def decree_mail(request):
    documents = Decree.objects.order_by('-id')
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'decree_mail.html', {
        'documents': page_obj,
        'show_add_and_search': True,
        'page_name': 'decree_mail',
        'model_name': 'decree'.strip(),  # Pass the model name
    })


#Shared Functions:
def get_model_and_form(model_name):
    model_mapping = {
        'incoming': Incoming,
        'outgoing': Outgoing,
        'internal': Internal,
        'decree': Decree,
    }

    form_mapping = {
        'incoming': AddIncomingForm,
        'outgoing': AddOutgoingForm,
        'internal': AddInternalForm,
        'decree': AddDecreeForm,
    }

    model = model_mapping.get(model_name.lower())
    form_class = form_mapping.get(model_name.lower())

    return model, form_class

def get_documents_with_files():
    results = Document.objects.filter(Q(pdf_file__isnull=False) | Q(attachment__isnull=False))
    return results

def get_document_details(request, model_type, document_id):
    model, _ = get_model_and_form(model_type)
    
    if model is None:
        return JsonResponse({'error': 'Invalid model type'}, status=400)

    document = get_object_or_404(model, id=document_id)

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


def add_document(request, model_name, document_id=None):
    model, form_class = get_model_and_form(model_name)
    
    if model is None or form_class is None:
        return HttpResponseNotFound('Invalid model name')

    form = form_class(request.POST or None, request.FILES or None, instance=document_id and get_object_or_404(model, id=document_id))

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'{model_name}_mail')  # Adjust this as needed
        else:
            logger.error(f"Form errors: {form.errors}")

    return render(request, f'add_edit_doc.html', {'form': form, 'model_name': model_name})


def edit_document(request, model_name, document_id):
    model, form_class = get_model_and_form(model_name)
    
    if model is None or form_class is None:
        return HttpResponseNotFound('Invalid model name')

    document = get_object_or_404(model, id=document_id)
    form = form_class(request.POST or None, request.FILES or None, instance=document)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            logger.info(f"Document {document_id} updated successfully.")
            return redirect(f'{model_name}_mail')  # Redirect based on model
        else:
            logger.error(f"Form errors: {form.errors}")

    return render(request, f'add_{model_name}.html', {'form': form})


def delete_document(request, model_name, document_id):
    model, _ = get_model_and_form(model_name)
    
    if model is None:
        return HttpResponseNotFound('Invalid model name')

    if request.method == 'DELETE':
        document = get_object_or_404(model, id=document_id)
        document.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


#download functions.

def download_document(request, model_name, object_id):
    model, _ = get_model_and_form(model_name)
    
    if model is None:
        return HttpResponseNotFound('Invalid model name')

    document = get_object_or_404(model, pk=object_id)

    # Determine the naming components
    date_str = document.date.strftime('%Y-%m-%d') if hasattr(document, 'date') and document.date else 'unknown_date'
    identifier = document.number if hasattr(document, 'number') else 'unknown'

    # Check for PDF and attachment
    pdf_exists = hasattr(document, 'pdf_file') and document.pdf_file
    attach_exists = hasattr(document, 'attach') and document.attach

    if not pdf_exists and not attach_exists:
        # Neither PDF nor attachment exist; return a 404 response
        return JsonResponse({'error': 'No document or attachment available for download.'}, status=404)

    if pdf_exists and attach_exists:
        # Both PDF and attachment exist; create a zip file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Add the PDF file to the zip
            pdf_filename = f"{model_name}_pdf_{identifier}_{date_str}.pdf"
            with document.pdf_file.open('rb') as pdf_file:
                zip_file.writestr(pdf_filename, pdf_file.read())

            # Add the attachment file to the zip
            attach_filename = f"{model_name}_attach_{identifier}_{date_str}.{document.attach.name.split('.')[-1]}"
            with document.attach.open('rb') as attach_file:
                zip_file.writestr(attach_filename, attach_file.read())

        # Prepare the zip response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{model_name}_{identifier}_{date_str}.zip"'
        
        return response

    elif pdf_exists:
        # Only PDF exists; download it
        content_type, _ = mimetypes.guess_type(document.pdf_file.name)
        if content_type is None:
            content_type = 'application/pdf'  # Default to PDF if unknown

        filename = f"{model_name}_pdf_{identifier}_{date_str}.pdf"
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with document.pdf_file.open('rb') as pdf_file:
            response.write(pdf_file.read())

        return response

    elif attach_exists:
        # Only attachment exists; download it
        content_type, _ = mimetypes.guess_type(document.attach.name)
        if content_type is None:
            content_type = 'application/octet-stream'  # Default to binary if unknown

        attach_filename = f"{model_name}_attach_{identifier}_{date_str}.{document.attach.name.split('.')[-1]}"
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{attach_filename}"'

        with document.attach.open('rb') as attach_file:
            response.write(attach_file.read())

        return response

    # Fallback if nothing matches (this should be unreachable due to the initial check)
    return HttpResponseNotFound('No document or attachment available for download.')