# admin.py
from django.contrib import admin
from .models import User,Attachment,Ticket

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Attachment)
