from django.shortcuts import render, redirect
from .forms import add_outgoing_form


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
            return redirect('index')  # Redirect back to the same form
    else:
        form = add_outgoing_form()
    
    return render(request, 'add_outgoing.html', {'form': form})