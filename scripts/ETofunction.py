import math

###################
#                 #
#   CONSTANTES    #
#                 #
###################
sigma = 4.903e-9   # Constante de Stefan–Boltzmann 

# Pressão de Saturação do vapor
def pressaosaturacaovapor(T):
    return 0.6108 * math.exp((17.27 * T) / (T + 237.3))

# Temperatura do ponto de orvalho
def temp_orvalho(e_s,RH):
    e_a = e_s*(RH/100.0)
    return (116.91 + 237.3 * math.log(e_a)) / (16.78 - math.log(e_a)) 

# Declinação da curva de Pressão de Saturação do vapor 
def Deltaes(Tm):
    return 4098 * (0.6108 * math.exp((17.27 * Tm) / (Tm + 237.3))) / ((Tm + 237.3) ** 2)

# Pressão atmosférica em função de Altitude
def PressaoATM(Z):
    return 101.3 * (((293 - 0.0065 * Z) / 293) ** 5.26)

# Constante psicrométrica
def Gama(P):
    return 0.665E-3 * P

# Dia Juliano
def diaJuliano(data):
  return  data.timetuple().tm_yday

# Distância Relativa terra-sol
def drterrasol(J):
    return 1 + 0.033 * math.cos(2 * math.pi * J / 365)
 
 # Declinação Solar
def declinasolar (J):
    return 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)

# Ângulo solar 
def angulosolar(phi, declina):
     return math.acos(-math.tan(phi) * math.tan(declina))

# Radiação Solar no topo da atmosfera 
def RadTopoAtm(phi, deltarad,dr,ws):
        return(24 * 60 / math.pi) * 0.0820 * dr * (ws * math.sin(phi) * math.sin(deltarad) + math.cos(phi) * math.cos(deltarad) * math.sin(ws))
# Balanço de Radiação de Ondas Curteas
def Boc(Rg):
    return (1 - 0.23) * Rg

# Balanço de Radiação de Ondas Longas
def Bol(Tx, Tn, ea, Rg,Ra, alt):
     return sigma * (((Tx + 273.16)**4 + (Tn + 273.16)**4)/2) * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * (Rg / ((0.75 + 2e-5 * alt) * Ra)) - 0.35)

# Saldo de Radiação
def SaldoRad(Rns, Rnl):
    return Rns - Rnl
# Cálculo da ETo — Método Penman-Monteith FAO56
def calcular_eto_pm_fao56(Tmed, Tmax, Tmin, UR, u, Rg, lat, alt,data):
       # =========================
            # CONSTANTES
       # =========================
        G = 0              # Fluxo de calor no solo - valor zero para a escala díaria      
        #Pressão de Saturação do vapor para Tmax e Tmin        
        es_Tmax = pressaosaturacaovapor(Tmax)
        es_Tmin = pressaosaturacaovapor(Tmin)
        # Pressão de Saturação do vapor média
        es = (es_Tmax + es_Tmin) / 2
        # Pressão de vapor atual
        e_a = es * (UR / 100)
        #Temperatura do ponto de orvalho
        Tdew=temp_orvalho(es,UR)
        # Pressão atual do vapor
        ea = pressaosaturacaovapor(Tdew)
        # Declinação da curva de Pressão de Saturação do vapor 
        delta = Deltaes(Tmed)
        #Pressão do vapor em função de Altitude
        P = PressaoATM(alt)
        # Constante psicrométrica
        gamma = Gama(P)
        # Dia Juliano
        J =  diaJuliano(data)
        # Distância Relativa terra-sol
        dr = drterrasol(J)
        # Transformação Graus para Radianos
        phi = math.radians(lat)
        # Declinação Solar 
        delta_rad = declinasolar (J)
        # Ângulo solar
        ws = angulosolar(phi, delta_rad)
        # Radiação Solar no topo da atmosfera 
        Ra = RadTopoAtm(phi, delta_rad,dr,ws)
        # Balanço de Radiação de Ondas Curteas
        Rns = Boc(Rg)
        # Balanço de Radiação de Ondas Longas
        Rnl = Bol(Tmax, Tmin, ea, Rg, Ra,alt,)
        # Saldo de Radiação
        Rn =SaldoRad(Rns,Rnl)
        # ETo Penman-Monteith
        eto = (0.408 * delta * (Rn - G) + gamma * (900 / (Tmed + 273)) * u * (es - ea)) / (delta + gamma * (1 + 0.34 * u))
        return round(max(0, eto), 2)

# Cálculo da ETo — Método Hargreaves-Samani (1985)
def calcular_eto_HS_1985(Tmed, Tmax, Tmin, lat,data):
        J =  diaJuliano(data)
        # Distância Relativa terra-sol
        dr = drterrasol(J)
        # Transformação Graus para Radianos
        phi = math.radians(lat)
        # Declinação Solar 
        delta_rad = declinasolar (J)
        # Ângulo solar
        ws = angulosolar(phi, delta_rad)
        # Radiação Solar no topo da atmosfera 
        Ra = RadTopoAtm(phi, delta_rad,dr,ws)
        # ETo Hargreaves-Samani Original
        eto = 0.0023*(Tmax - Tmin)**(0.5)*(Tmed + 17.8)*Ra*0.408
        return round(max(0, eto), 2)

# Cálculo da ETo — Método Hargreaves-Samani modificado por Jensen et al (1985)
def calcular_eto_HSJ_1997(Tmed, Tmax, Tmin, u, lat,data):
        a,b = 0.175, 0.066
        J =  diaJuliano(data)
        # Distância Relativa terra-sol
        dr = drterrasol(J)
        # Transformação Graus para Radianos
        phi = math.radians(lat)
        # Declinação Solar 
        delta_rad = declinasolar (J)
        # Ângulo solar
        ws = angulosolar(phi, delta_rad)
        # Radiação Solar no topo da atmosfera 
        Ra = RadTopoAtm(phi, delta_rad,dr,ws)
        # ETo Hargreaves-Samani Original
        eto = (a+b*u)*(0.0023*(Tmax - Tmin)**(0.5)*(Tmed + 17.8)*Ra*0.408)
        return round(max(0, eto), 2)

# Cálculo da ETo — Método Hargreaves-Samani modificado por Jensen et al (1985)
def calcular_eto_HSLJ_2020(Tmed, Tmax, Tmin, RH, lat,data):
        a,b = 0.175, 0.066
        J =  diaJuliano(data)
        # Distância Relativa terra-sol
        dr = drterrasol(J)
        # Transformação Graus para Radianos
        phi = math.radians(lat)
        # Declinação Solar 
        delta_rad = declinasolar (J)
        # Ângulo solar
        ws = angulosolar(phi, delta_rad)
        # Radiação Solar no topo da atmosfera 
        Ra = RadTopoAtm(phi, delta_rad,dr,ws)
        # ETo Hargreaves-Samani Original
        eto = (1/(a+b*RH))*(0.0023*(Tmax - Tmin)**(0.5)*(Tmed + 17.8)*Ra*0.408)
        return round(max(0, eto), 2)

    
