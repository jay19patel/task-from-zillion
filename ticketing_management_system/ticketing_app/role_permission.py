from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

class RoleRequiredMixin(UserPassesTestMixin):
    role = "staff"

    def test_func(self):
        if self.role == "any":
            return self.request.user.is_authenticated
        return self.request.user.is_authenticated and self.request.user.role == self.role

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('not_authorized')
        else:
            return super().handle_no_permission()
