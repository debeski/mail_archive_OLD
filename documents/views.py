from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import AddOutgoingForm, AddIncomingForm, AddInternalForm, AddDecreeForm, AddReportForm, DepartmentForm, AffiliateForm, MinisterForm, GovernmentForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import mimetypes
from django.apps import apps
from .models import Incoming, Outgoing, Internal, Decree, Report, Department, Affiliate, Minister, Government
import logging
from django.utils import timezone
from io import BytesIO
import zipfile
from django.core.paginator import Paginator
from django.db.models import Q
import plotly.express as px
import pandas as pd
from django.utils.http import urlencode





logger = logging.getLogger('documents')



# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)



# Function to map models, forms, arabic names and data:
def get_model_data(model_name):
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

    # Get model, form, and arabic names
    model = model_mapping.get(model_name.lower())
    form_class = form_mapping.get(model_name.lower())
    arabic_name = arabic_name_mapping.get(model_name.lower())
    arabic_names = arabic_name_mapping

    # Initialize data
    model_data = {
        'documents': None,
        'distinct_years': [],
        'ministers': None,
        'governments': None,
    }
    # Fill in the data
    if model:
        # Check if the model supports soft deletion
        if hasattr(model, 'deleted_at'):
            documents = model.objects.filter(deleted_at__isnull=True)
        else:
            documents = model.objects.all()  # No soft deletion
        model_data['documents'] = documents

        # Gather distinct years if the model has a date field
        model_data['distinct_years'] = documents.dates('date', 'year') if hasattr(model, 'date') else []

        # Gather ministers for the Decree model
        if model.__name__.lower() == 'decree':
            model_data['ministers'] = Minister.objects.all()

        if model.__name__.lower() == 'decree':
            model_data['governments'] = Government.objects.all()



    return model, form_class, arabic_name, arabic_names, model_data



# Function to create Chart for index:
def create_chart():
    # Define model names
    model_classes = [Outgoing, Incoming, Internal, Decree, Report]
    years = range(2008, 2025)
    data = []

    # Fetch counts and Arabic names using get_model_name
    for model in model_classes:
        arabic_name = model().get_model_name

        # Count documents for each year
        for year in years:
            count = model.objects.filter(date__year=year, deleted_at__isnull=True).count() or 0
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
    fig.update_layout(
        selectdirection='h',
        height=370,
        title=dict(font=dict(size=30), automargin=True),
        title_x=0.55,  # Center the title
        xaxis_title='',
        yaxis_title='عدد الوثائق',

        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0,
            yanchor='bottom'
        ),
        hoverlabel=dict(
            align='right',  # Align hover text to the right
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



# Html & Chart Rendering Functions on main page only:
def index(request):
    # Generate the chart HTML
    chart_html = create_chart()  # Get the chart HTML

    # Define model names based on the mapping in get_model_data
    model_names = ['incoming', 'outgoing', 'internal', 'decree', 'report']
    
    latest_documents = []

    for model_name in model_names:
        model, _, _, _, _ = get_model_data(model_name)
        latest_documents += list(model.objects.order_by('-created_at')[:5])

    # Limit to the latest 5 documents across all models
    latest_documents = sorted(latest_documents, key=lambda x: x.created_at, reverse=True)[:5]

    return render(request, 'index.html', {
        'latest_documents': latest_documents,
        'chart_html': chart_html,  # Include the chart HTML in the context
    })



# Function for Sections Management:
def manage_sections(request, model_name):
    current_tab = request.GET.get('tab', model_name)

    # Fetch model, form class, arabic name, and arabic names
    model, form_class, arabic_name, arabic_names, _ = get_model_data(current_tab)

    # Wrap arabic_name in a dictionary if it’s a string
    if isinstance(arabic_name, str):
        arabic_name = {current_tab: arabic_name}

    # Handle document editing
    document_id = request.GET.get('id')
    form = form_class(request.POST or None, instance=get_object_or_404(model, id=document_id) if document_id else None)

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        form.save()  # This will handle saving the many-to-many relationships
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



def document_view(request, model_name):
    # Get model data
    model, form_class, arabic_name, arabic_names, model_data = get_model_data(model_name)

    # Default values for sorting, filtering, and pagination
    sort_option = request.GET.get('sort', 'updated_at')  # Default sort by
    order = request.GET.get('order', 'desc')  # Default order
    keyword_search = request.GET.get('keyword_search', '')
    year_filter = request.GET.get('year', '')
    minister_filter = request.GET.get('minister', '')
    government_filter = request.GET.get('government', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')


    # Filter documents based on search term and soft delete logic
    documents = model.objects.filter(deleted_at__isnull=True) if hasattr(model, 'deleted_at') else model.objects.all()

    # Apply filters
    if keyword_search:
        # Start with the base query
        query = Q(title__icontains=keyword_search) | Q(keywords__icontains=keyword_search) | Q(number__icontains=keyword_search)
        # Check if the model has the 'special_field' attribute
        if hasattr(model, 'orig_number'):
            query |= Q(orig_number__icontains=keyword_search)
        # Apply the combined query to filter documents
        documents = documents.filter(query)

    use_alternate = request.GET.get('use_alternate') == 'on'

    # Determine which date field to use
    if use_alternate and hasattr(model, 'orig_date'):
        date_field = 'orig_date'
    elif hasattr(model, 'date'):
        date_field = 'date'
    else:
        date_field = None

    # Apply year filter if the model has the selected date field
    if year_filter and date_field:
        documents = documents.filter(**{f'{date_field}__year': year_filter})

    # Apply date range filter if the model has the selected date field
    if start_date and end_date and date_field:
        documents = documents.filter(**{f'{date_field}__range': [start_date, end_date]})

    if minister_filter:
        documents = documents.filter(minister__id=minister_filter)

    if government_filter:
        documents = documents.filter(government__id=government_filter)


    # Calculate new_order based on sort_option and order dynamically
    new_order = 'asc' if order == 'desc' else 'desc'

    # Apply sorting
    documents = documents.order_by(f'-{sort_option}' if order == 'desc' else sort_option)

    # Pagination logic
    paginator = Paginator(documents, 10)  # 10 documents per page
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)  # Convert to integer
    except ValueError:
        page_number = 1  # Default to the first page if conversion fails
    page_obj = paginator.get_page(page_number)

    for doc in page_obj.object_list:
        pdf_file_exists = getattr(doc, 'pdf_file', None) is not None
        attach_exists = getattr(doc, 'attach', None) is not None
        doc.has_file = bool(pdf_file_exists and doc.pdf_file.name) or bool(attach_exists and doc.attach.name)

    # Fetch the distinct years for the dropdown and ministers if applicable
    distinct_years = model_data['distinct_years']
    ministers = model_data['ministers']
    governments = model_data['governments']

    # Prepare query parameters
    query_params = {
        'keyword_search': request.GET.get('keyword_search', ''),
        'year': request.GET.get('year', ''),
        'minister': request.GET.get('minister', ''),
        'government': request.GET.get('government', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'sort': sort_option,  # Use the value from the request or default
        'order': order,
        'use_alternate': use_alternate,
    }


    # Encode the parameters using urlencode
    query_string = urlencode({k: v for k, v in query_params.items() if v})

    print("Query String:", query_string)

    return render(request, 'documents.html', {
        'documents': page_obj.object_list,
        'page_obj': page_obj,
        'keyword_search': keyword_search,
        'year_filter': year_filter,
        'minister_filter': minister_filter,
        'government_filter': government_filter,
        'start_date': start_date,
        'end_date': end_date,
        'distinct_years': distinct_years,
        'ministers': ministers,
        'governments': governments,
        'model_name': model_name,
        'arabic_name': arabic_name,
        'arabic_names': arabic_names,
        'query_string': query_string,
        'sort_option': sort_option,
        'order': order,
        'new_order': new_order,
    })


# Function to add a new entry or edit an existing one:
def add_document(request, model_name, document_id=None):
    model, form_class, arabic_name, _, _ = get_model_data(model_name)
    
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


# Function to delete an entry:
def delete_document(request, model_name, document_id):
    model, _, _, _, _ = get_model_data(model_name)

    if model is None:
        return HttpResponseNotFound('Invalid model name')

    if request.method == 'DELETE':
        doc = get_object_or_404(model, id=document_id)
        doc.deleted_at = timezone.now()  # Set the deletion timestamp
        doc.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Function to download pdf or zip file:
def download_document(request, model_name, object_id):
    model, _, _, _, _ = get_model_data(model_name)
    
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
