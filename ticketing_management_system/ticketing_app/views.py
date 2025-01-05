# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .role_permission import RoleRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,DeleteView,UpdateView
from django.contrib import messages
from .models import User
from django.views import View
from django.urls import reverse_lazy,reverse
from .models import Ticket,Attachment
import uuid
class RegisterView(RoleRequiredMixin,View):
    template_name = 'registration.html'
    role = "admin"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        decription = request.POST.get('decription')
        if not username or not email or not decription:
            messages.error(request, "All fields are required.")
            return redirect("registration")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("registration")
        
        user = User.objects.create_user(username=username, email=email,decription=decription, password="temp123")
        user.save()
        messages.success(request, "Registration successful.")
        return redirect('manage_staff')

class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("user.is_handover",user.is_handover)
            if user.is_handover:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')
            
            messages.warning(request,"Change Your Password")
            url = reverse('change_password') + f'?username={username}'
            return redirect(url)


        else:
            messages.warning(request, "Invalid credentials.")
        
        return render(request, self.template_name)
    
class ChangePassword(View):
    template_name = 'change_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.GET.get('username')
        if password1 != password2:
            messages.warning("Password dose not match. try agin")
            return redirect("change_password")
        
        user = authenticate(request, username=username, password="temp123")
        if user:
            print("is_handover", user.is_handover)
            user.is_handover = True
            user.set_password(password2)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect('login')
        else:
            messages.warning(request, "Something went to wrong. !")
        
        return render(request, self.template_name)

class NotAuthorized(TemplateView):
    template_name = "not_authorized.html"
    
class HomeView(RoleRequiredMixin,TemplateView):
    template_name = 'home.html'
    login_url = reverse_lazy('login')
    role = "any"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['email'] = user.role       
        context['username'] = user.username 
        print(Ticket.objects.filter(status = "Ongoing").count(),"<---------") 
        if user.role == "admin" :    
            context['total_tickets'] = Ticket.objects.all().count()
            context['ongoing_tickets'] = Ticket.objects.filter(status = "Ongoing").count()          
            context['complated_tickets'] =Ticket.objects.filter(status = "Complated").count()      
            context['archived_tickets'] = Ticket.objects.filter(status = "Archived").count()        
        else:       
            context['total_tickets'] = Ticket.objects.filter(assigned_member=user).count()
            context['ongoing_tickets'] = Ticket.objects.filter(status = "Ongoing",assigned_member=user).count()          
            context['complated_tickets'] =Ticket.objects.filter(status = "Completed",assigned_member=user).count()    
        return context

class ManageTickets(RoleRequiredMixin, TemplateView):
    role = "any"
    template_name = 'manage_tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        
        status_param = self.kwargs.get('status', None)
        if status_param == "All":
            context["tickets"] = Ticket.objects.all()
        else:
            context["tickets"] = Ticket.objects.filter(status=status_param)
        
        context["column_name"] = ["Id", "Title", "Assigned To", "Status", "-"]
        return context


class ManageStaff(RoleRequiredMixin, ListView):
    model = User
    template_name = 'manage_staff.html'
    context_object_name = 'users'
    role = "admin"

    def get_queryset(self):
        return User.objects.filter(role='staff')
    
    def get_context_data(self, *args,**kwargs):
        
        context = super().get_context_data(**kwargs)
        context["column_name"] = ["name","username","email","status","action"]
        return context

class CreateTickets(RoleRequiredMixin,View):
    template_name = 'create_tickets.html'
    role = "admin"

    def get(self, request, *args, **kwargs):
        context = {
            'users': User.objects.filter(role='staff')
        }
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_member_username = request.POST.get('assigned_member')
        attachments = request.FILES.getlist('attachments')
        try:
            uuid_str = str(uuid.uuid4())[:15]
            if assigned_member_username == "0":
                ticket = Ticket.objects.create(
                    id=f"Ticket-{uuid_str}",
                    title=title,
                    description=description,
                    assigned_member = None,
                    status='Draft',
                )
            else:
                ticket = Ticket.objects.create(
                    id=f"Ticket-{uuid_str}",
                    title=title,
                    description=description,
                    assigned_member = User.objects.get(username=assigned_member_username),
                    status='Ongoing',
                )
            for file in attachments:
                ticket.attachments.create(file=file)


            messages.success(request, "Ticket created and assigned successfully!")
            return redirect(reverse('manage_tickets', kwargs={'status': 'All'})) 
        except User.DoesNotExist:
            messages.error(request, "Assigned member not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        context = {
            'users': User.objects.filter(role='staff'),
        }
        return render(request, self.template_name, context)
    

class ViewTickets(RoleRequiredMixin,DetailView):
    model=Ticket
    template_name="view_ticket.html"
    role="any"
    context_object_name = 'ticket'

class DeleteTicket(RoleRequiredMixin,DeleteView):
    role="admin"
    model = Ticket
    template_name = 'ticket_confirm_delete.html'
    context_object_name = 'ticket'
    def get_success_url(self):
        return reverse_lazy('manage_tickets', kwargs={'status': "All"})
    def get_object(self, queryset=None):
        ticket_id = self.kwargs['pk']
        return Ticket.objects.get(id=ticket_id)
    

class SolveTicket(View):
    template_name = 'solve_ticket.html'
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        print("---------------------",id)
        context = {"ticket" :Ticket.objects.get(id=id)}
        print(context)
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        solution = request.POST.get('solution')
        attachments = request.FILES.getlist('attachments')
        id = self.kwargs.get('pk')

        ticket = Ticket.objects.get(id=id)
        print(ticket)
        print(solution)
        if ticket and solution:
            print(solution)
            ticket.solution = solution
            ticket.status = "Completed"
            for file in attachments:
                    ticket.attachments.create(file=file)
            ticket.save()
            return redirect(reverse('manage_tickets', kwargs={'status': 'Complated'}))
        else:
            messages.warning(request,"Solution not fount try again.")
        