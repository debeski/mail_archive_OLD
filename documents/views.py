from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
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
