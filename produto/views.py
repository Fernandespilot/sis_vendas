from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProdutoForm
from .models import Produto
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Produto

def lista_produtos(request):
    # Pega os parâmetros do GET
    nome = request.GET.get('nome', '')
    preco_min = request.GET.get('preco_min', '')
    preco_max = request.GET.get('preco_max', '')

    # Query inicial
    produtos = Produto.objects.all()

    # Aplica filtro por nome (contém, case insensitive)
    if nome:
        produtos = produtos.filter(nome__icontains=nome)

    # Filtra preço mínimo, se válido
    if preco_min:
        try:
            preco_min_val = float(preco_min)
            produtos = produtos.filter(preco__gte=preco_min_val)
        except ValueError:
            pass

    # Filtra preço máximo, se válido
    if preco_max:
        try:
            preco_max_val = float(preco_max)
            produtos = produtos.filter(preco__lte=preco_max_val)
        except ValueError:
            pass

    # Ordena os produtos por nome
    produtos = produtos.order_by('nome')

    # Paginação (5 itens por página)
    paginator = Paginator(produtos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto para template, com dados do filtro para manter os inputs preenchidos
    context = {
        'page_obj': page_obj,
        'nome': nome,
        'preco_min': preco_min,
        'preco_max': preco_max,
    }

    return render(request, 'produto/lista_produtos.html', context)


def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva no banco
            return redirect('lista_produtos')  # Redireciona para a lista após salvar
    else:
        form = ProdutoForm()
    return render(request, 'produto/cadastrar_produto.html', {'form': form})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/editar_produto.html', {'form': form})

@require_POST
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return JsonResponse({'success': True})


