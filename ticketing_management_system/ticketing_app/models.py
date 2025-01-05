from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    is_active = models.BooleanField(default=True)
    is_handover = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    decription = models.TextField(max_length=200,default="You Are Awsome")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attachment(models.Model):
    STATUS_CHOICES = (
        ('Ticket', 'Ticket'),
        ('Solution', 'Solution'),
        ('Completed', 'Completed'),
        ('Archived', 'Archived'),
    )
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey('Ticket',on_delete=models.CASCADE,related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Archived', 'Archived'),
    )
    id = models.CharField(max_length=30,primary_key=True)
    title = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_member = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    solution = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

