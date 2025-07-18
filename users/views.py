from django.contrib import auth

# Função de logout baseada no exemplo do usuário
def logout(request):
    auth.logout(request)
    return redirect('login')
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


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

@login_required
def password_change(request):
    if request.method == 'POST':
        if request.POST.get('clear_success'):
            request.session.pop('show_password_success', None)
            return redirect('password_change')
        form = PasswordChangeForm(user=request.user, data=request.POST)
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        requisitos = []
        if new_password1:
            if len(new_password1) >= 8:
                requisitos.append('comprimento')
            if any(c.isdigit() for c in new_password1):
                requisitos.append('digito')
            if any(c.isupper() for c in new_password1):
                requisitos.append('maiuscula')
            if any(c.islower() for c in new_password1):
                requisitos.append('minuscula')
        if new_password1 != new_password2:
            messages.error(request, 'Os campos Nova Senha e Confirmar Senha devem ser iguais.')
        elif not all(r in requisitos for r in ['comprimento','digito','maiuscula','minuscula']):
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres, incluir dígitos, letras maiúsculas e minúsculas.')
        elif form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso!')
            request.session['show_password_success'] = True
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})

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
