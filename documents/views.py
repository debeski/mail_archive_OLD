from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import AddOutgoingForm, AddIncomingForm, AddInternalForm, AddDecreeForm, AddReportForm, DepartmentForm, AffiliateForm, MinisterForm, GovernmentForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import mimetypes
from django.apps import apps
from .models import Incoming, Outgoing, Internal, Decree, Report, Department, Affiliate, Minister, Government
import logging
from django.utils import timezone
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np
import os
from django.conf import settings
from io import BytesIO
import zipfile
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd




logger = logging.getLogger('documents')



# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)



# Function to map models, forms, and arabic names:
def get_model_and_form(model_name):
    model_mapping = {
        'incoming': Incoming,
        'outgoing': Outgoing,
        'internal': Internal,
        'decree': Decree,
        'report': Report,

        'departments': Department,
        'affiliates': Affiliate,
        'governments': Government,
        'ministers': Minister,
    }

    form_mapping = {
        'incoming': AddIncomingForm,
        'outgoing': AddOutgoingForm,
        'internal': AddInternalForm,
        'decree': AddDecreeForm,
        'report': AddReportForm,

        'departments': DepartmentForm,
        'affiliates': AffiliateForm,
        'governments': GovernmentForm,
        'ministers': MinisterForm,
    }

    arabic_name_mapping = {
        'incoming': "بريد وارد",
        'outgoing': "بريد صادر",
        'internal': "مذكرة داخلية",
        'decree': "قرار",
        'report': "تقرير",

        'departments': "الاقسام",
        'affiliates': "الجهات",
        'governments': "الحكومة",
        'ministers': "الوزير",
    }

    model = model_mapping.get(model_name.lower())
    form_class = form_mapping.get(model_name.lower())
    arabic_name = arabic_name_mapping.get(model_name.lower())

    arabic_names = arabic_name_mapping  # Add this to pass the full dictionary for pluralization


    return model, form_class, arabic_name, arabic_names



# def create_chart():
#     # Define model names
#     model_names = ['incoming', 'outgoing', 'internal', 'decree', 'report']
#     years = range(2018, 2025)
#     counts = {model: [] for model in model_names}

#     # Create a Plotly figure
#     fig = go.Figure()

#     # Fetch counts and Arabic names using get_model_and_form
#     for model_name in model_names:
#         model, _, arabic_name, _ = get_model_and_form(model_name)  # Get the Arabic name directly
        
#         # Count documents for each year
#         for year in years:
#             count = model.objects.filter(date__year=year).count() or 0
#             counts[model_name].append(count)

#         # Add a bar for each model using the returned Arabic name directly
#         fig.add_trace(go.Bar(
#             name=arabic_name,  # Use the Arabic name directly here
#             x=list(years),
#             y=counts[model_name],
#             width=0.1,
#             offsetgroup=model_names.index(model_name)  # Offset by group
#         ))

#     # Update layout for RTL
#     fig.update_layout(
#         title=dict(text="عدد الوثائق حسب السنة", font=dict(size=30), automargin=True, yref='container'),
#         title_x=0.55,  # Center the title
#         xaxis_title='السنة',  # X-axis title in Arabic
#         yaxis_title='عدد الوثائق',  # Y-axis title in Arabic
#         barmode='group',
#         xaxis=dict(tickvals=list(years), title_standoff=15),  # Set x-axis ticks to match years
#         legend=dict(
#             orientation='h',  # Horizontal legend
#             x=0.5,  # Center horizontally
#             xanchor='center',  # Anchor center
#             y=-0.2,  # Position below the chart
#             yanchor='top',
#             indentation=100,
#             itemtext=1
#         ),
#         autosize=True,  # Enable autosizing
#         margin=dict(l=50, r=50, t=40, b=0),  # Set margins
#         font=dict(family='Shabwa, sans-serif', size=16, color='black'),  # Font settings
#     )

#     # Convert the figure to HTML and return it
#     return fig.to_html(full_html=False)

def create_chart():
    # Define model names
    model_classes = [Incoming, Outgoing, Internal, Decree, Report]
    years = range(2018, 2025)
    data = []

    # Fetch counts and Arabic names using get_model_and_form
    for model in model_classes:
        arabic_name = model().get_model_name

        # Count documents for each year
        for year in years:
            count = model.objects.filter(date__year=year).count() or 0
            data.append({'Year': year, 'Count': count, 'Model': arabic_name})

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create a Plotly Express bar chart
    fig = px.bar(
        df,
        x='Year',
        y='Count',
        color='Model',
        barmode='group',
        title='عدد الوثائق حسب السنة',
        labels={'Year': 'السنة', 'Count': 'عدد الوثائق'},
        text='Count',
        hover_name='Model',
        hover_data={'Model':False}
    )

    # Update layout for RTL
    # Update layout for RTL
    fig.update_layout(
        selectdirection='h',
        height=420,
        title=dict(font=dict(size=30), automargin=True),
        title_x=0.55,  # Center the title
        xaxis_title='السنة',
        yaxis_title='عدد الوثائق',

        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.2,
            yanchor='top'
        ),
        hoverlabel=dict(
            align='auto',  # Align hover text to the right
            bgcolor='rgba(255, 255, 255, 0.8)',  # Background color
            bordercolor='black',  # Border color
            font=dict(size=14, color='black')  # Font settings
        ),
        autosize=True,  # Enable autosizing
        margin=dict(l=50, r=50, t=40, b=0),  # Set margins
        font=dict(family='Shabwa, sans-serif', size=16, color='black'),  # Font settings
    )

    # Convert the figure to HTML and include the dynamic hover label script
    chart_html = fig.to_html(full_html=False)
    # JavaScript for dynamic hover label positioning
    dynamic_hover_script = """
    <script>
        const myDiv = document.getElementById('myDiv');
        myDiv.on('plotly_hover', function(eventData) {
            const hoverLabel = document.querySelector('.hovertext'); // Select the hover label
            if (hoverLabel) {
                const mouseX = eventData.event.clientX; // Get mouse X position
                const mouseY = eventData.event.clientY; // Get mouse Y position

                // Adjust hover label position
                hoverLabel.style.left = `${mouseX + 30}px`; // Add small offset
                hoverLabel.style.top = `${mouseY + 40}px`;  // Add small offset
            }
        });
    </script>
    """

    return chart_html + dynamic_hover_script


# Html & Chart Rendering Functions:
def index(request):
    # Generate the chart HTML
    chart_html = create_chart()  # Get the chart HTML

    # Define model names based on the mapping in get_model_and_form
    model_names = ['incoming', 'outgoing', 'internal', 'decree', 'report']
    
    latest_documents = []

    for model_name in model_names:
        model, _, _, _ = get_model_and_form(model_name)
        latest_documents += list(model.objects.order_by('-created_at')[:5])

    # Limit to the latest 5 documents across all models
    latest_documents = sorted(latest_documents, key=lambda x: x.created_at, reverse=True)[:5]

    return render(request, 'index.html', {
        'latest_documents': latest_documents,
        'chart_html': chart_html,  # Include the chart HTML in the context
    })



# Sections Management:
def manage_sections(request, model_name):
    current_tab = request.GET.get('tab', model_name)

    # Fetch model, form class, arabic name, and arabic names
    model, form_class, arabic_name, arabic_names = get_model_and_form(current_tab)

    # Wrap arabic_name in a dictionary if it’s a string
    if isinstance(arabic_name, str):
        arabic_name = {current_tab: arabic_name}

    # Handle document editing
    document_id = request.GET.get('id')
    form = form_class(request.POST or None, instance=get_object_or_404(model, id=document_id) if document_id else None)

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('manage_sections', model_name=current_tab)

    # Fetch items for the current tab's model with pagination
    items = model.objects.all()
    paginator = Paginator(items, 10)
    page_number = request.GET.get(f'{current_tab}_page', 1)  # Use current_tab for pagination
    page_obj = paginator.get_page(page_number)

    return render(request, 'manage_sections.html', {
        'models': [
            {'name': 'departments', 'form': DepartmentForm(), 'items': Department.objects.all()},
            {'name': 'affiliates', 'form': AffiliateForm(), 'items': Affiliate.objects.all()},
            {'name': 'ministers', 'form': MinisterForm(), 'items': Minister.objects.all()},
            {'name': 'governments', 'form': GovernmentForm(), 'items': Government.objects.all()},
        ],
        'current_tab': current_tab,
        'form': form,
        'page_obj': page_obj,
        'request': request,
        'arabic_name': arabic_name,
        'arabic_names': arabic_names,  # Ensure this is a dictionary
        f'{current_tab}_page': page_number,  # Use current_tab for pagination
        'arabic_name_value': arabic_name.get(current_tab, 'اسم غير معروف')
    })



# Check for File Existence:
def has_files(instance):
    model_name = instance.__class__.__name__.lower()  # Get the model name in lowercase
    model, _, _, _ = get_model_and_form(model_name)  # Use get_model_and_form to get the model

    if model is None:
        print(f"Model not found for instance: {instance}")
        return False

    # Check for files based on model type
    if model_name == 'incoming' or model_name == 'outgoing' or model_name == 'internal' or model_name == 'report':
        has_file = hasattr(instance, 'pdf_file') and bool(instance.pdf_file)
        print(f"Checking {model_name.capitalize()}: {has_file} (pdf: {instance.pdf_file if has_file else 'N/A'})")
        return has_file
    elif model_name == 'decree':
        pdf_file_exists = hasattr(instance, 'pdf_file') and bool(instance.pdf_file)
        attach_exists = hasattr(instance, 'attach') and bool(instance.attach)
        has_file = pdf_file_exists or attach_exists
        print(f"Checking Decree: {has_file} (pdf: {pdf_file_exists}, attach: {attach_exists})")
        return has_file

    return False



# General Html Mail Rendering Function:
def document_view(request, model_name):
    model, _, arabic_name, _ = get_model_and_form(model_name)

    if model is None:
        return HttpResponseNotFound('Invalid model name')

    # Get all instances of the specified model that are not soft deleted
    documents = model.objects.filter(deleted_at__isnull=True)  # Filter out soft deleted documents

    # Handle search query
    search_term = request.GET.get('search', '').strip()
    if search_term:
        documents = documents.filter(
            Q(title__icontains=search_term) | 
            Q(date__icontains=search_term) | 
            Q(number__icontains=search_term) | 
            Q(updated_at__icontains=search_term)
        )

    # Determine sort option and order
    sort_option = request.GET.get('sort', 'updated_at')  # Default sort
    order = request.GET.get('order', 'desc')  # Default order

    if sort_option == 'date':
        documents = documents.order_by('-date' if order == 'desc' else 'date')
    elif sort_option == 'number':
        documents = documents.order_by('-number' if order == 'desc' else 'number')
    elif sort_option == 'title':
        documents = documents.order_by('-title' if order == 'desc' else 'title')
    elif sort_option == 'updated_at':
        documents = documents.order_by('-updated_at' if order == 'desc' else 'updated_at')

    # Pagination setup
    paginator = Paginator(documents, 15)
    page_number = request.GET.get('page', 1)  # Default to first page
    page_obj = paginator.get_page(page_number)

    # Generate a list of tuples (document, has_files)
    documents_with_files = [(doc, has_files(doc)) for doc in page_obj]

    return render(request, 'documents.html', {
        'documents_with_files': documents_with_files,
        'model_name': model_name,
        'arabic_name': arabic_name,  # Pass the Arabic name to the template
        'page_obj': page_obj,         # Pass the page object for pagination controls
        'sort_option': sort_option,    # Pass the current sort option to the template
        'order': order,                # Pass the current order to the template
        'search_term': search_term      # Pass the search term to the template
    })



def add_document(request, model_name, document_id=None):
    model, form_class, arabic_name, _ = get_model_and_form(model_name)
    
    if model is None or form_class is None:
        return HttpResponseNotFound('Invalid model name')

    if document_id:
        instance = get_object_or_404(model, id=document_id)  # Editing existing document
    else:
        instance = None  # New document

    form = form_class(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('document_view', kwargs={'model_name': model_name}))  # Use reverse to construct URL
        else:
            logger.error(f"Form errors: {form.errors}")

    return render(request, f'add_edit_doc.html', {
        'form': form, 
        'model_name': model_name, 
        'arabic_name': arabic_name,
    })



def delete_document(request, model_name, document_id):
    model, _, _, _ = get_model_and_form(model_name)

    if model is None:
        return HttpResponseNotFound('Invalid model name')

    if request.method == 'DELETE':
        document = get_object_or_404(model, id=document_id)
        document.deleted_at = timezone.now()  # Set the deletion timestamp
        document.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



def download_document(request, model_name, object_id):
    model, _, _, _ = get_model_and_form(model_name)
    
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



# Gather information for Details Pane Function:
# def get_document_details(request, model_type, document_id):
#     model, _, _ = get_model_and_form(model_type)
    
#     if model is None:
#         return JsonResponse({'error': 'Invalid model type'}, status=400)

#     document = get_object_or_404(model, id=document_id)

#     # Prepare the response data based on the model type
#     data = {
#         'id': document.id,
#         'number': document.number,
#         'date': document.date.strftime('%Y-%m-%d') if document.date else None,
#         'title': document.title,
#         'keywords': document.keywords,
#         'pdf_file': document.pdf_file.url if document.pdf_file else None,
#     }

#     # Add specific fields based on the model
#     if isinstance(document, Incoming):
#         data.update({
#             'orig_number': document.orig_number,
#             'orig_date': document.orig_date.strftime('%Y-%m-%d') if document.orig_date else None,
#             'dept_from': document.dept_from.name,
#             'dept_to': document.dept_to.name,
#         })
#     elif isinstance(document, Outgoing):
#         data.update({
#             'dept_from': document.dept_from.name,
#             'dept_to': document.dept_to.name,
#         })
#     elif isinstance(document, Internal):
#         data.update({
#             'dept_from': document.dept_from.name,
#             'dept_to': document.dept_to.name,
#         })
#     elif isinstance(document, Decree):
#         data.update({
#             'minister': document.minister.name,
#             'government': document.government.name,
#             'attach_file': document.attach.url if document.attach else None,
#         })

#     return JsonResponse(data)
