from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
# from django.db.models import Q
import plotly.express as px
import pandas as pd
# from django.utils.http import urlencode
from .llm_service import llm_service_instance
import speech_recognition as sr
from django.core.cache import cache



logger = logging.getLogger('documents')



# Logger initiation Function:
def log_action(action, model, object_id=None):
    timestamp = timezone.now()
    message = f"{timestamp} - Performed {action} on {model.__name__} (ID: {object_id})"
    logger.info(message)


def user_login(request):
    user_name = None  # Initialize the variable to store the user's name

    # If the user is already authenticated, redirect to index
    if request.user.is_authenticated:
        if request.user.is_staff:  # Admin users (staff) shouldn't use the login modal
            logger.info(f"Admin {request.user.username} is already logged in.")
            return redirect('admin:index')  # Redirect admin to the admin dashboard
        logger.info(f'User {request.user.username} is already authenticated.')
        return redirect('index')  # Redirect to the index page

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next')  # Get the next URL from the form
        logger.debug(f'Attempting to authenticate user: {username}')  # Log the username attempt
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_name = user.username
            logger.info(f'User {username} logged in successfully.')  # Log successful login

            if 'show_login_modal' in request.session:
                del request.session['show_login_modal']

            # Always redirect to index after login
            return redirect(next_url or 'index')
        else:
            messages.error(request, 'Invalid username or password.')
            logger.warning(f'Failed login attempt for user: {username}')

    # Render the index page with the login form if not authenticated
    return render(request, 'index.html', {'user_name': user_name})


def clear_login_modal_flag(request):
    """ Clear the session flag to prevent the modal from showing again. """
    if request.method == 'POST':  # We expect a POST request to clear the session flag
        if 'show_login_modal' in request.session:
            del request.session['show_login_modal']
        return JsonResponse({'message': 'Login modal flag cleared'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


# Function to map models, forms, arabic names and data:
def get_model_data(model_name=None):
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

    # arabic_name_mapping = {
    #     'incoming': "بريد وارد",
    #     'outgoing': "بريد صادر",
    #     'internal': "مذكرة داخلية",
    #     'decree': "قرار",
    #     'report': "تقرير",

    #     'departments': "الاقسام",
    #     'affiliates': "الجهات",
    #     'governments': "الحكومة",
    #     'ministers': "الوزير",
    # }


    if model_name:
        model_class = model_mapping.get(model_name.lower())
        form_class = form_mapping.get(model_name.lower())
        if not model_class:
        # Return None if model_name is not recognized
            return None, None, None, None
    else:
        # Return all models and forms if model_name is not provided
        return list(model_mapping.values()), None, None, None
    
    # Return requested model , form, and arabic names
    arabic_name = model_class._meta.verbose_name
    arabic_names = model_class._meta.verbose_name_plural
    # arabic_names = arabic_name_mapping

    return model_class, form_class, arabic_name, arabic_names


# Function to create Chart for index:
def create_chart():
    cache_key = 'chart_data'

    # Check if the chart data is cached
    chart_html = cache.get(cache_key)
    
    if chart_html is None:
        # Your existing code to create the chart
        years = range(2008, 2025)
        data = []

        model_names = ['incoming', 'outgoing', 'internal', 'decree', 'report']
        for model_name in model_names:
            model_class, _, arabic_name, _ = get_model_data(model_name)

            # Count documents for each year
            for year in years:
                count = model_class.objects.filter(date__year=year, deleted_at__isnull=True).count() or 0
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
            hover_data={'Model': False}
        )

        # Update layout for RTL and other settings
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
                align='right',
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='black',
                font=dict(size=14, color='black')
            ),
            autosize=True,
            margin=dict(l=50, r=50, t=40, b=0),
            font=dict(family='Shabwa, sans-serif', size=16, color='black'),
        )

        # Convert the figure to HTML
        chart_html = fig.to_html(full_html=False)

        # Store the generated chart HTML in the cache
        cache.set(cache_key, chart_html, timeout=3600)  # Cache for 1 hour

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
    chart_html = create_chart()

    # Define model names similar to the mapping in get_model_data
    model_names = ['incoming', 'outgoing', 'internal', 'decree', 'report']
    # Initialize an empty list
    latest_documents = []
    # Populate the list with latest added documents
    for model_name in model_names:
        model_class, _, arabic_name, _ = get_model_data(model_name)
        documents = list(model_class.objects.order_by('-created_at')[:5])
        for document in documents:
            latest_documents.append((document, arabic_name))  # or use model_name based on your needs

    # Limit to the latest 5 documents across all models
    latest_documents = sorted(latest_documents, key=lambda x: x[0].created_at, reverse=True)[:5]

    return render(request, 'index.html', {
        'latest_documents': latest_documents,
        'chart_html': chart_html,
    })


# Function for Sections Management:
def manage_sections(request, model_name):
    # Initialize a new variable with current tab
    current_tab = request.GET.get('tab', model_name)

    # Fetch model_class, form class, arabic name, and arabic names
    model_class, form_class, arabic_name, arabic_names = get_model_data(current_tab)

    # Handle document editing
    document_id = request.GET.get('id')
    form = form_class(request.POST or None, instance=get_object_or_404(model_class, id=document_id) if document_id else None)
    edited = True if document_id else False

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('manage_sections', model_name=current_tab)

    # Fetch items for the current tab's model with pagination
    items = model_class.objects.all()
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page', 1)  # Using current_tab for pagination
    page_obj = paginator.get_page(page_number)

    return render(request, 'manage_sections.html', {
        'models': [
            {'name': 'departments', 'form': DepartmentForm(), 'items': Department.objects.all(), 'ar_name': Department._meta.verbose_name_plural},
            {'name': 'affiliates', 'form': AffiliateForm(), 'items': Affiliate.objects.all(), 'ar_name': Affiliate._meta.verbose_name_plural},
            {'name': 'ministers', 'form': MinisterForm(), 'items': Minister.objects.all(), 'ar_name': Minister._meta.verbose_name_plural},
            {'name': 'governments', 'form': GovernmentForm(), 'items': Government.objects.all(), 'ar_name': Government._meta.verbose_name_plural},
        ],
        'current_tab': current_tab,
        'form': form,
        'page_obj': page_obj,
        'request': request,
        'arabic_name': arabic_name,
        'arabic_names': arabic_names,
        'total_pages': paginator.num_pages,
        'edited': edited,
    })


# Function that handles main display of tables, fetches filters from LLMservice, searches through models:
def document_view(request, model_name):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    # llm_service = llm_service_instance

    # Initialize model_class and related variables
    model_class, _, arabic_name, arabic_names = None, None, None, None

    # Get model data only if model_name is valid
    if model_name:
        model_class, _, arabic_name, arabic_names = get_model_data(model_name)

    # Initialize filters dictionary
    filters = {
        'start_date': request.GET.getlist('start_date'),
        'end_date': request.GET.getlist('end_date'),
        'keywords': request.GET.getlist('keywords'),
        'minister': request.GET.get('minister'),
        'affiliate': request.GET.get('affiliate'),
        'department': request.GET.get('department'),
        'government': request.GET.get('government'),
        'model_choice': [label for label in request.GET]
    }

    # Get the natural language query from the request
    nlq = request.GET.get('search', '')
    logger.info(f"Submitted Query: {nlq}")

    # Check for audio input (if using a mic icon, you might have a separate endpoint for that)
    if request.method == 'POST' and 'audio' in request.FILES:
        # Handle audio input
        audio_file = request.FILES['audio']
        nlq = process_audio_input(audio_file)  # Convert audio to text
        logger.info("Processed audio input to text.")

    relevant_documents = model_class.objects.none()  # Initialize as an empty queryset

    if nlq:
        predicted_labels = llm_service.process_query(nlq)
        filters = llm_service.extract_filters_from_labels(nlq, predicted_labels)
        logger.info(f"Extracted Labels: {predicted_labels}")  # Log the extracted labels
        logger.info(f"Extracted Filters: {filters}")  # Log the extracted filters

        # Get model choices from filters
        model_choices = filters.get('model_choice', [])

        if model_choices:
            # Fetch documents for each model class based on model_choices
            for choice in model_choices:
                model_class_info = get_model_data(choice)
                if model_class_info[0]:  # Check if model_class is not None
                    documents = llm_service.fetch_documents(filters)  # Fetch documents using the filters
                    if documents is not None:
                        relevant_documents = relevant_documents | documents  # Combine querysets
                        logger.info(f"Fetched documents for model choice: {choice}.")
        else:
            # If no specific models are chosen, fetch documents from all models
            all_models = get_model_data()  # Get all models
            for model_class in all_models:
                documents = llm_service.fetch_documents(filters)  # Fetch documents using the filters
                if documents is not None:
                    relevant_documents = relevant_documents | documents  # Combine querysets
                    logger.info(f"Fetched documents for all models.")
    else:
        if model_class:
            relevant_documents = model_class.objects.all()  # Only fetch from the specific model if it exists

    # Apply the deleted_at filter now
    if hasattr(model_class, 'deleted_at'):
        relevant_documents = relevant_documents.filter(deleted_at__isnull=True)

    # Default values for sorting and filtering
    sort_option = request.GET.get('sort', 'updated_at')  # Default sort by
    order = request.GET.get('order', 'desc')  # Default order

    # Calculate new_order based on sort_option and order dynamically
    new_order = 'asc' if order == 'desc' else 'desc'
    # Apply sorting
    relevant_documents = relevant_documents.order_by(f'-{sort_option}' if order == 'desc' else sort_option)
    if sort_option == 'number':
        # Sort using the integer value from get_last_segment
        relevant_documents = sorted(relevant_documents, key=lambda x: x.get_last_segment(), reverse=(order == 'desc'))

    # Pagination logic
    paginator = Paginator(relevant_documents, 10)  # 10 documents per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    for doc in page_obj:
        pdf_file_exists = getattr(doc, 'pdf_file', None) is not None
        attach_exists = getattr(doc, 'attach', None) is not None
        doc.has_file = bool(pdf_file_exists and doc.pdf_file.name) or bool(attach_exists and doc.attach.name)

    logger.info(f"Returned {page_obj.paginator.count} documents for model '{model_name}'.")

    return render(request, 'documents.html', {
        'documents': page_obj,
        'page_obj': page_obj,
        'model_name': model_name,
        'arabic_name': arabic_name,
        'arabic_names': arabic_names,
        'sort_option': sort_option,
        'order': order,
        'new_order': new_order,
        'nlq': nlq,
        'total_pages': paginator.num_pages,
    })

def process_audio_input(audio_file):
    """Convert audio input to text using speech recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # Read the entire audio file
    # Recognize speech using Google Web Speech API
    try:
        text = recognizer.recognize_google(audio, language='ar-LB')  # Use appropriate Arabic locale
        return text
    except sr.UnknownValueError:
        return ""  # Return empty string if speech is unintelligible
    except sr.RequestError:
        return ""  # Return empty string in case of API request error


# Function to add a new entry or edit an existing one:
def add_document(request, model_name, document_id=None):
    model_class, form_class, arabic_name, _ = get_model_data(model_name)
    
    if model_class is None or form_class is None:
        return HttpResponseNotFound('Invalid model name')

    if document_id:
        instance = get_object_or_404(model_class, id=document_id)  # Editing existing document
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
    model_class, _, _, _ = get_model_data(model_name)

    if model_class is None:
        return HttpResponseNotFound('Invalid model name')

    if request.method == 'DELETE':
        doc = get_object_or_404(model_class, id=document_id)
        doc.deleted_at = timezone.now()  # Set the deletion timestamp
        doc.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Function to download pdf or zip file:
def download_document(request, model_name, object_id):
    model_class, _, _, _ = get_model_data(model_name)
    
    if model_class is None:
        return HttpResponseNotFound('Invalid model name')

    document = get_object_or_404(model_class, pk=object_id)

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
