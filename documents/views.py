from django.shortcuts import render

# Create your views here.

from .models import Incoming, Outgoing, Internal, Decree

from django.shortcuts import render, redirect
from .forms import add_decree_form

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

def add_decree(request):
    if request.method == 'POST':
        form = add_decree_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('decrees')  # Change to your success URL
    else:
        form = add_decree_form()
    
    return render(request, 'decrees.html', {'form': form})