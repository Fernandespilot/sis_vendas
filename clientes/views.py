from django.shortcuts import render

def lista_clientes(request):
    return render(request, 'clientes/lista_clientes.html')

