# urls.py
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = "login"), name='logout'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('not_authorized/', NotAuthorized.as_view(), name='not_authorized'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('', HomeView.as_view(), name='home'),
    path('manage_staff/', ManageStaff.as_view(), name='manage_staff'),
    path('manage_tickets/<str:status>/', ManageTickets.as_view(), name='manage_tickets'),
    path('create_tickets/', CreateTickets.as_view(), name='create_tickets'),
    path('view_ticket/<str:pk>/', ViewTickets.as_view(), name='view_ticket'),
    path('delete_ticket/<str:pk>/', DeleteTicket.as_view(), name='delete_ticket'),
    path('solve_ticket/<str:pk>/', SolveTicket.as_view(), name='solve_ticket'),
]
