from django.shortcuts import render
"""
""
, redirect, get_object_or_404
from apps.solos.models import Solo
from apps.solos.forms import SoloForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator

# Função para verificar se é superusuário
def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(
        lambda u: u.is_superuser,
        login_url='/admin/login/',
        redirect_field_name=None
    )(view_func))
    return decorated_view_func

@superuser_required
def novo_solo(request):
    if request.method == 'POST':
        form = SoloForm(request.POST)
        if form.is_valid():
            solo = form.save()
            messages.success(request, f'Solo "{solo.nome}" cadastrado com sucesso!')
            return redirect('solos/lista_solos.html')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SoloForm()
    
    return render(request, 'solos/form_solos.html', {'form': form, 'titulo': 'Cadastrar Novo Solo'})

@superuser_required
def editar_solo(request, solo_id):
    solo = get_object_or_404(Solo, id=solo_id)
    
    if request.method == 'POST':
        form = SoloForm(request.POST, instance=solo)
        if form.is_valid():
            solo = form.save()
            messages.success(request, f'Solo "{solo.nome}" atualizado com sucesso!')
            return redirect('lista_solos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SoloForm(instance=solo)
    
    return render(request, 'solos/form_solos.html', {'form': form, 'titulo': 'Editar Solo'})

@superuser_required
def lista_solos(request):
    solos = Solo.objects.all().order_by('-data_cadastro')
    
    # Paginação
    paginator = Paginator(solos, 10)  # 10 solos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'solos/lista_solos.html', {'page_obj': page_obj})

@superuser_required
def excluir_solo(request, solo_id):
    solo = get_object_or_404(Solo, id=solo_id)
    
    if request.method == 'POST':
        nome_solo = solo.nome
        solo.delete()
        messages.success(request, f'Solo "{nome_solo}" excluído com sucesso!')
        return redirect('lista_solos')
    
    return render(request, 'solos/confirmar_exclusao.html', {'solo': solo})
    """
