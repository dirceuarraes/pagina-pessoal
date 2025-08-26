from django.shortcuts import render, get_object_or_404, redirect

#pagina principal
def index(request):
    return render(request, 'perfil/index.html')
