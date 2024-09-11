from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')

#login
@ensure_csrf_cookie
def submit_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválido")
    return HttpResponse('Invalid request')

#filtra e mostra os eventos do usuario
@login_required(login_url='/login/')
def home(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(request, "home.html", dados)

#Adiciona um evento
@login_required(login_url='/login/')
def submit_evento(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario)
    return redirect('/')

#Exclui um evento
def destroy(request):
    if request.method == "POST":
        evento_id = request.POST.get('evento_id')
        Evento.objects.filter(id=evento_id).delete()
        return redirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})