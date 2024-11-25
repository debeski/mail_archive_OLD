from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Incoming, Outgoing, Internal, Decree

admin.site.register(Incoming)
admin.site.register(Outgoing)
admin.site.register(Internal)
admin.site.register(Decree)