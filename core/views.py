from core.models import Evento
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie
import re
from datetime import datetime, timedelta

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

#Ainda falta eu descobrir como colocar os dados já salvos nesse "evento"
#Provavel que seja algo no html, depois vejo isso
@login_required(login_url='/login/')
def evento(request):
    evento_id = request.GET.get('id', '')
    evento_id = re.sub(r'[^\d]', '', evento_id) # Remove caracteres não numéricos
    dados = {}
    return render(request, 'evento.html', dados)

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
def submit_evento(request):             #Por algum motivo não está atualizando os dados
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        evento_id = request.POST.get('evento_id')
        print(f"evento_id: {evento_id}")
        if evento_id:
            Evento.objects.filter(id=evento_id).update(titulo=titulo, data_evento=data_evento, descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario)
    return redirect('/')

#Exclui um evento
@login_required(login_url='/login/')
def destroy(request):
    usuario = request.user
    evento_id = request.POST.get('evento_id')
    evento = Evento.objects.get(id=evento_id)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')

#registra um novo usuario
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

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = requesr.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual)
    dados = {'eventos':evento}
    return render(request, 'home.html', dados)