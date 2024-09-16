from django.urls import path
from django.views.generic import RedirectView
from .views import login_user, submit_login, logout_user, evento, home, submit_evento, destroy, register

urlpatterns = [
    path('home/', home, name='home'),
    path('', RedirectView.as_view(url='/home/')),
    path('home/evento/', evento, name='evento'),
    path('home/evento/submit', submit_evento, name='submit_evento'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('login/submit', submit_login, name='submit'),
    path('logout/', logout_user, name='logout'),
    path('destroy', destroy, name='destroy')

]