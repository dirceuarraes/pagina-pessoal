import math
def fswamee(Rey, diametro,rugosidade):
    relativa = rugosidade/diametro
    return ((64/Rey)**8+9.5*(math.log(relativa/3.7+5.74/Rey**0.9)-(2500/Rey)**6)**(-16))**0.125


def calReynolds(vazao,diametro):
     pi=math.pi
     viscosidade = 1.004E-6
     velocidade = 4*vazao/(pi*diametro**2)
     return velocidade*diametro/viscosidade

#Calculo da perda de carga pela equação de Darcy-Weisbach
def calDarcyWeisbach(vazao, diametro, comprimento, rugosidade, F):
    #CONSTANTES 
    g = 9.81   
    pi = math.pi 
   
    Reynolds = calReynolds(vazao,diametro)
    
    f = fswamee(Reynolds, diametro,rugosidade)

    print(f)
    return (8*f/(pi**2*g))*vazao**2/diametro**5*comprimento*F 

#Calculo da perda de carga pela equação de Hazen-Williams
def calHazenWilliams(vazao, diametro, comprimento, C,F):
    return 10.641*(vazao/C)**1.852*comprimento/diametro**4.87*F

#Calculo da perda de carga pela equação de Flammant
def calFlammant(vazao, diametro, comprimento, F):
    return  0.00082510*vazao**1.75*comprimento/diametro**4.75*F

# Calculo de diâmetro pela equação de Darcy=Weisbach
def caldiametroDW(vazao,perdacargamax,comprimento, rugosidade,F):
    #CONSTANTES 
    g = 9.81   
    pi = math.pi 
    erro = 1E-4
    teste = True
    velocidade = 1.5
    diametro = math.sqrt(4*vazao/(pi*velocidade))
   
    Reynolds = calReynolds(vazao,diametro)
    it =0
    f = fswamee(Reynolds, diametro,rugosidade)
    diametronovo = ((8*f/(pi**2*g)*vazao**2*comprimento*F/perdacargamax))**(1/5)
    while teste:
        diametroantigo =  diametronovo        
        Reynolds = calReynolds(vazao,diametroantigo)
        f = fswamee(Reynolds, diametroantigo,rugosidade)
        diametronovo = ((8*f/(pi**2*g)*vazao**2*comprimento*F/perdacargamax))**(1/5)
        errocal = abs((diametroantigo-diametronovo)/diametronovo)
        if (errocal<erro) or (it>1000):
            teste = False
        it+=1
    diametro = diametronovo
    return diametro

# Calculo de diâmetro pela equação de Hazen-Williams
def caldiametroHW(vazao,perdacargamax,comprimento, Chw,F):
    return ((10.641*(vazao/Chw)**1.852*comprimento*F)/perdacargamax)**(1/4.87)

#Calculo do diâmetro pela equação de Flammant
def caldiametroFL(vazao,perdacargamax,comprimento,F):
    return (0.00082510*vazao**1.75*comprimento*F/perdacargamax)**(1/4.75)

#calculo do fator de correção
def Fcorrecao(Ne,ev):
    return 1/ev+1/(2*Ne)+(math.sqrt(ev-1))/(6*Ne**2)

#Diametro adotado PEAD 
def CalDLLadotadoPEAD(D):
    if D<=0.013:
        Da = 0.013
    elif 0.013 < D <= 0.016:
        Da = 0.016
    elif  0.016 < D <= 0.019:
        Da = 0.019
    else:
        Da = 0.022
    return Da

#Diametro adotado demais materiais 
def CalDLLadotadomateriais(Dcal):
    if Dcal<=0.025:
        Da = 0.025
    elif 0.025 < Dcal <= 0.035:
        Da = 0.035
    else:
        Da = (int(Dcal/0.025)+1)*0.025
    return Da