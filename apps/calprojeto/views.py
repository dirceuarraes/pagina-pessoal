from django.shortcuts import render
from django.contrib import messages
from apps.calprojeto.forms import CalProjetoForms
from scripts.rotinas import calDarcyWeisbach,calHazenWilliams, calFlammant,caldiametroDW,caldiametroHW,caldiametroFL,Fcorrecao
from scripts.rotinas import CalDLLadotadomateriais, CalDLLadotadoPEAD
import math

# Dicionário com os valores de rugosidade (em mm)

RUGOSIDADES = {
    'AC': 0.045,    # Aço comercial (novo)
    'AF': 0.045,    # Aço forjado (novo)
    'AFO': 0.60,    # Aço forjado (oxidado)
    'AG': 0.15,     # Aço galvanizado (novo)    
    'AGO': 0.15,    # Aço galvanizado (usado)
    'PVC': 0.0015,  # PVC
    'PEAD': 0.007,  # Polietileno (PEAD)
    'FE': 0.25,     # Ferro fundido (novo)
    'FEO': 1.00,    # Ferro fundido (usado)
}

# Coeficientes C de Hazen-Williams (valores típicos)
CHW = {
    'AC': 130,    # Aço comercial (novo)
    'AF': 130,    # Aço forjado (novo)
    'AFO': 100,   # Aço forjado (oxidado)
    'AG': 125,    # Aço galvanizado (novo)
    'AGO': 120,   # Aço galvanizado (usado)
    'PVC': 150,   # PVC
    'PEAD': 150,  # Polietileno (PEAD)
    'FE': 130,    # Ferro fundido (novo)
    'FEO': 100,   # Ferro fundido (usado)
}
def CalProjeto(request):
    Resultados = None
    nome = None
    form = CalProjetoForms()
    if request.method == 'POST':
        form = CalProjetoForms(request.POST)

        if form.is_valid():
            #Sistema 
            sistema=form.cleaned_data['sistema']
            qemissor = form.cleaned_data['qemissor']
            PS = form.cleaned_data['PS']
            Ee = form.cleaned_data['Ee']
            EL = form.cleaned_data['EL']
            AlturaEmissor = form.cleaned_data['AlturaS'] 
            Fator = form.cleaned_data['Fator']/100.0           
            Qdisp = form.cleaned_data['Qdisp']
            #Linha Lateral (Layout)
            materialLL = form.cleaned_data['materialLL']
            metodosLL = form.cleaned_data['metodosLL']
            comprimentoLL = form.cleaned_data['comprimentoLL']
            declividadeLL = form.cleaned_data['declividadeLL']/100.0
            #Linha derivação
            materialLDPS = form.cleaned_data['materialLDPS']
            metodosLDPS = form.cleaned_data['metodosLDPS']
            comprimentoLD = form.cleaned_data['comprimentoLD']
            declividadeLD = form.cleaned_data['declividadeLD']/100.0
            linhasdoissentidos = form.cleaned_data['linhasdoissentidos']
            #Linha Principal
            comprimentoLP = form.cleaned_data['comprimentoLD']
            declividadeLP = form.cleaned_data['declividadeLD']/100.0
            velocidademax = form.cleaned_data['velocidademax']
            #Linha de Sucção
            comprimentoLS = form.cleaned_data['comprimentoLS']
            AlturaS = form.cleaned_data['AlturaS']
            
            #Sistema de Irrigação
            if sistema=="ILM":
                nome = "Microaspersão"
            elif sistema=="ILG":
                nome = "Gotejamento"
            else:
                nome = "Aspersão Convencional"
            
            # Número de emissores
            Ne = int(comprimentoLL/Ee)
            # Vazão da linha
            QLL = Ne*qemissor
            # Número de Linhas Laterais
            if  linhasdoissentidos =="sim":
                NLL=int(comprimentoLD/EL)*2
            else:
                NLL=int(comprimentoLD/EL)
            #Vazão do projeto
            Qproj = NLL*QLL
            Ns = 0
            if Qproj>Qdisp:
                #Adicionar uma mensagem de alerta na tela avisando que é necessário dividir a área em setores
                Ns = int(Qproj/Qdisp)+1
                messages.warning(
                    request,
                    f"Número de setores calculado: {Ns}. Ajuste LL/LD e envie novamente."
                )
                return render(request, 'calprojeto/CalProjeto.html', {'form':form,'Resultados':Resultados,})
            
           #------------------------------------------------------------------------------------------------------
            # Perda de Carga máxima na linha lateral
            hfmax = 0.2*PS+declividadeLL*comprimentoLL
            if hfmax<0:
                 messages.warning(
                    request,
                    f"Critério de 20%PS não é : {hfmax}. É necessário usar outro critério de calculo."
                )
                 return render(request, 'calprojeto/CalProjeto.html', {'form':form,'Resultados':Resultados,})
        
            #calculo do fator F
            if metodosLL=="DW":
                Ev = 2.0
            elif metodosLL =="DH":
                Ev = 1.852
            else:
                Ev = 1.75
            Fcorr = Fcorrecao(Ne,Ev)
            
            #Calculo do diametro
            if metodosLDPS=="DW":
                rugosidade = RUGOSIDADES[materialLL]/1000.0
                DLLcal = caldiametroDW(QLL/(1000*3600),hfmax,comprimentoLL,rugosidade,Fcorr)
            elif metodosLDPS =="HZ":
                Chw = CHW[materialLL]
                DLLcal = caldiametroHW(QLL/(1000*3600),hfmax,comprimentoLL,Chw,Fcorr)
            else:
                DLLcal=caldiametroFL(QLL/(1000*3600),hfmax,comprimentoLL,Fcorr)
            print(DLLcal)
            #diametro adotado
            if  materialLL=="PEAD":
                DLLadot = CalDLLadotadoPEAD(DLLcal)
            else:
                DLLadot = CalDLLadotadomateriais(DLLcal)
            print(DLLadot)
            #Calculo da perda de carga na linha lateral 
            if metodosLL=="DW":                
                rugosidade = RUGOSIDADES[materialLDPS]/1000.0
                hfLL = calDarcyWeisbach(QLL/(1000*3600),DLLadot, comprimentoLL,rugosidade,Fcorr)
            elif metodosLL == "HZ":
                Chw = CHW[materialLDPS]
                hfLL = calHazenWilliams(QLL/(1000*3600),DLLadot,comprimentoLL,Chw,Fcorr)
            else:
                hfLL = calFlammant(QLL/(1000*3600),DLLadot,comprimentoLL,Fcorr)

            #Calculo da pressão no início da linha lateral
            PinLL = PS + 0.75*hfLL - declividadeLL*comprimentoLL/2+AlturaEmissor
            #---------------------------------------------------------------------
            #---------------------------------------------------------------------
            #--------------- Linha de Derivação ----------------------------------
            # Calculo perda de carga máxima na linha de Derivação
            hfmaxLD = 0.30*PS+declividadeLD*comprimentoLD
            
            #calculo do fator F
            if metodosLDPS=="DW":
                Ev = 2.0
            else: 
                Ev = 1.852
            Fcorr = Fcorrecao(NLL,Ev)
           
            
            #Calculo do diametro
            if metodosLDPS=="DW":
                rugosidade = RUGOSIDADES[materialLDPS]/1000.0
                DLDcal = caldiametroDW(Qproj/(1000*3600),hfmaxLD,comprimentoLD,rugosidade,Fcorr)
            else:
                Chw = CHW[materialLDPS]
                #print(Qproj, comprimentoLD, hfmaxLD, Fcorr, metodosLDPS,Chw)
                DLDcal = caldiametroHW(Qproj/(1000*3600),hfmaxLD,comprimentoLD,Chw,Fcorr)
            
            #diametro adotado
            if  materialLDPS=="PEAD":
                DLDadot = CalDLLadotadoPEAD(DLDcal)
            else:
                DLDadot = CalDLLadotadomateriais(DLDcal)

            #Calculo da perda de carga na linha derivação
            if metodosLDPS=="DW":                
                rugosidade = RUGOSIDADES[materialLDPS]/1000.0
                hfLD = calDarcyWeisbach(Qproj/(1000*3600),DLDadot, comprimentoLD,rugosidade,Fcorr)
            else:
                Chw = CHW[materialLDPS]
                hfLD = calHazenWilliams(Qproj/(1000*3600),DLDadot,comprimentoLD,Chw,Fcorr)

            #---------------------------------------------------------------------
            #---------------------------------------------------------------------
            #--------------- Linha de Principal ----------------------------------
            #Calculo do diâmtro pelo critério de velocidade ----------------------
            velocidadeLP = 4*Qproj/(math.pi*DLDadot**2)
            if velocidadeLP<=velocidademax:
                DLPadot = DLDadot
            else:          
                DLPcal = math.sqrt((4*Qproj/(1000.0*3600.0))/(math.pi*velocidademax))
                #diametro adotado
                if  materialLDPS=="PEAD":
                    DLPadot = CalDLLadotadoPEAD(DLPcal)
                else:
                    DLPadot = CalDLLadotadomateriais(DLPcal)
            
            #Calculo da perda de carga na linha principal
            if metodosLDPS=="DW":                
                rugosidade = RUGOSIDADES[materialLDPS]/1000.0
                hfLP = calDarcyWeisbach(Qproj/(1000*3600),DLPadot, comprimentoLP,rugosidade,Fcorr)
            else:
                Chw = CHW[materialLDPS]
                hfLP = calHazenWilliams(Qproj/(1000*3600),DLPadot,comprimentoLP,Chw,Fcorr)
                        
            #---------------------------------------------------------------------
            #---------------------------------------------------------------------
            #--------------- Linha de Sucção -------------------------------------
            #Diâmetro da linha de Sucção -----------------------------------------
            DLSadot = DLPadot + 0.025

            #Calculo da perda de carga na linha de Sucção
            if metodosLDPS=="DW":                
                rugosidade = RUGOSIDADES[materialLDPS]/1000.0
                hfLS = calDarcyWeisbach(Qproj/(1000*3600),DLSadot, comprimentoLS,rugosidade,Fcorr)
            else:
                Chw = CHW[materialLDPS]
                hfLS = calHazenWilliams(Qproj/(1000*3600),DLSadot,comprimentoLS,Chw,Fcorr)

            #Altura de Recalque
            Hrecalque = comprimentoLP*declividadeLP+comprimentoLD*declividadeLD
            #Calculo da Altura manométrica (Hm)
            Hm = (1+Fator)*(PinLL+hfLD+hfLP+hfLS+AlturaS+Hrecalque) 

           

            Resultados = {
                "resumo": {
                    "sistema": nome,
                    "Ne": Ne, "NLL": NLL, "Ns": Ns,
                    "QLL": QLL, "Qproj": Qproj, "Qdisp": Qdisp,
                },
                "lateral": {                                   
                    "DLLadot": DLLadot,
                    "hfLL": hfLL,
                    "PinLL":PinLL,
                },
                 "derivacao": {
                    "hfmaxLD": hfmaxLD,
                    "DLDcal": DLDcal,
                    "DLDadot": DLDadot,
                    "hfLD": hfLD,
                 },  # preencha se calcular
                 "principal": {
                    "DLPadot": DLPadot,
                    "hfLP": hfLP,
                 },  # preencha se calcular
                 "succao": {
                    "DLSadot": DLSadot,
                    "hfLS": hfLS,
                    "Hm":Hm
                 },     # preencha se calcular
            }
              

    return render(request, 'calprojeto/CalProjeto.html', {'form':form,'Resultados':Resultados,})