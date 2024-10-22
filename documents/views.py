from django.shortcuts import render, redirect, get_object_or_404
from .forms import add_outgoing_form
from django.http import HttpResponse, HttpResponseNotFound
import mimetypes


from .models import Incoming, Outgoing, Internal, Decree

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

# documents/views.py

def add_outgoing(request):
    if request.method == 'POST':
        form = add_outgoing_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('outgoing_mail')  # Redirect back to the same form
    else:
        form = add_outgoing_form()
    
    return render(request, 'add_outgoing.html', {'form': form})

def outgoing_mail(request):
    documents = Outgoing.objects.all()  # Use the correct model name here
    return render(request, 'outgoing_mail.html', {'documents': documents})

def download_outgoing_pdf(request, outgoing_id):
    """
    Downloads a PDF file based on its ID.

    Args:
        request (django.http.HttpRequest): The HTTP request object.
        outgoing_id (int): The ID of the Outgoing object to download.

    Returns:
        django.http.HttpResponse: The HTTP response containing the PDF file.
    """

    outgoing = get_object_or_404(Outgoing, pk=outgoing_id)

    # Check if the file exists and is a PDF
    if outgoing.pdf_file and outgoing.pdf_file.name.endswith('.pdf'):
        # Use mimetypes to get the content type
        content_type, _ = mimetypes.guess_type(outgoing.pdf_file.name)
        if content_type is None:
            content_type = 'application/pdf'  # Default to PDF if unknown

        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{outgoing.pdf_file.name}"'
        
        with outgoing.pdf_file.open('rb') as pdf_file:
            response.write(pdf_file.read())
        
        return response
    else:
        return HttpResponseNotFound('PDF file not found or invalid')
