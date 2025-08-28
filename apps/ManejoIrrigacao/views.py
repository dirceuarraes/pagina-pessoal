from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from apps.ManejoIrrigacao.forms import CalManejoForm   
from apps.culturas.models import Cultura
from apps.solos.models import Solo  
import math



def manejo_irrigacao(request):
    Resultados = {}   
    if request.method == 'POST':
        form = CalManejoForm(request.POST)
        if form.is_valid():
            cultura = form.cleaned_data['cultura']
            solo = form.cleaned_data['solo']
            fase = form.cleaned_data['fase']
            sistema = form.cleaned_data['sistema']
            VazaoEmissor = form.cleaned_data['VazaoEmissor']
            espacamentoEmissor = form.cleaned_data['espacamentoEmissor']
            espacamentoLinha = form.cleaned_data['espacamentoLinha']
            raiomolhado = form.cleaned_data['raiomolhado']
            Ea = form.cleaned_data['eficIrrigacao']
            Ea = Ea / 100  # Convertendo para decimal
            Uatual = form.cleaned_data['Uatual']


            #Agora vamos usar os dados do formulário para pegar as informações nos bancos de dados
            # Informações do Solo
            Ucc = solo.capacidade_campo

            if Uatual >= Ucc:
                messages.error(request, "A Umidade Atual não pode ser maior ou igual a Umidade em Capacidade de Campo.")
                return render(request, 'ManejoIrrigacao/manejo_irrigacao.html', {'form': form, 'Resultados': Resultados,})
            else:
            
                ds = solo.densidade
                # Informações da Cultura
                if fase == 'FI':
                # Kc = cultura.kc_inicial
                    Z = cultura.z_min*1000 # Convertendo para mm
            
                elif fase == 'FM':
               # Kc = cultura.kc_medio
                    Z = (cultura.z_min + cultura.z_max) / 2*1000 # Convertendo para mm
                else:
               # Kc = cultura.kc_final
                    Z = cultura.z_max*1000  # Convertendo para mm
            # Cálculos:
            # Lâmina Líquida (LL), 
                LL = (Ucc - Uatual)*ds*Z
            # Lâmina Bruta (LB)
                LB = LL/Ea
            # Área molhada (Am)
                if sistema == 'ILM' or sistema == 'ILG':
                    Am = math.pi * (raiomolhado**2)
                    Am=min(espacamentoEmissor* espacamentoLinha, math.pi * (raiomolhado**2))
                else:
                    Am = espacamentoEmissor * espacamentoLinha
            # Tempo de Irrigação (Ti)
                Ti = LB*Am/VazaoEmissor
                Horas = int(Ti)
                Min = int((Ti - Horas) * 60)
                Resultados = {                
                    'Z': round(Z, 2),
                    'LL': round(LL, 2),
                    'LB': round(LB, 2),
                    'Ti': f"{Horas} h e {Min} min",

            }
    else:
        form = CalManejoForm()
    return render(request, 'ManejoIrrigacao/manejo_irrigacao.html', {'form': form, 'Resultados': Resultados,})