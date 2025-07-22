from django.shortcuts import render, redirect, get_object_or_404
from .forms import PromotorForm
from .models import Promotor
from django.contrib.auth.models import User, Group

def cadastrar_promotor(request):
    if request.method == 'POST':
        form = PromotorForm(request.POST)
        if form.is_valid():
            # Cria o usuário do Django
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            nome = form.cleaned_data['nome']
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            # Adiciona o usuário ao grupo Promotor
            grupo_promotor, created = Group.objects.get_or_create(name='Promotor')
            user.groups.add(grupo_promotor)
            promotor = form.save(commit=False)
            promotor.user = user
            promotor.save()
            return redirect('lista_promotores')
    else:
        form = PromotorForm()
    return render(request, 'promotor/cadastrar_promotor.html', {'form': form})

def lista_promotores(request):
    promotores = Promotor.objects.all()
    return render(request, 'promotor/lista_promotores.html', {'promotores': promotores})

def editar_promotor(request, pk):
    promotor = get_object_or_404(Promotor, pk=pk)
    if request.method == 'POST':
        form = PromotorForm(request.POST, instance=promotor)
        if form.is_valid():
            form.save()
            return redirect('lista_promotores')
    else:
        form = PromotorForm(instance=promotor)
    return render(request, 'promotor/editar_promotor.html', {'form': form, 'promotor': promotor})

def visualizar_promotor(request, pk):
    promotor = get_object_or_404(Promotor, pk=pk)
    return render(request, 'promotor/visualizar_promotor.html', {'promotor': promotor})

def excluir_promotor(request, pk):
    promotor = get_object_or_404(Promotor, pk=pk)
    if request.method == 'POST':
        promotor.delete()
        return redirect('lista_promotores')
    return render(request, 'promotor/excluir_promotor.html', {'promotor': promotor})
