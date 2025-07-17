from django.contrib.auth.views import LogoutView

# Permitir logout via GET
class CustomLogoutView(LogoutView):
    next_page = '/login/'
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm

# Formulário de autenticação por email

class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['username'].widget.attrs['autofocus'] = True

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            self.cleaned_data['username'] = user.username
        except User.DoesNotExist:
            pass  # Deixe o erro padrão do AuthenticationForm acontecer
        return super().clean()


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailAuthenticationForm

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

@login_required
def perfil(request):
    user = request.user
    tipo = 'Administrador' if user.groups.filter(name='Administrador').exists() else 'Promotor'
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('perfil')
    return render(request, 'registration/perfil.html', {'user': user, 'tipo': tipo})
