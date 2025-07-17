
from django.shortcuts import render
from produto.models import Produto
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'core/home.html', {'produtos': produtos})
