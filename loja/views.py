from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import loja.models
from loja.models import Usuario, Roupas, Checkout



def index(request):

    if request.user.is_authenticated:

        usuario = get_object_or_404(Usuario, user=request.user.id)

        if Checkout.objects.filter(usuario=usuario).exists():

            carrinho = get_object_or_404(Checkout, usuario=usuario)
            listaCompras = carrinho.roupas.all()

            return render(request,'index.html',{'listaCompras':listaCompras})

        else:

            render(request, 'index.html', )

    else:

        render(request, 'index.html', )



def loginSite(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'loginfalhou.html')
    return render(request, 'logincerto.html')







