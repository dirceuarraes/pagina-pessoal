from django.shortcuts import render, get_object_or_404, redirect
from apps.calETo.forms import EToForms
from scripts.ETofunction import calcular_eto_pm_fao56,calcular_eto_HS_1985,calcular_eto_HSJ_1997,calcular_eto_HSLJ_2020


def ETo(request):
    resultado = None
    detalhe = None
    form = EToForms()

    if request.method == 'POST':
        form = EToForms(request.POST)

        if form.is_valid():
            data=form.cleaned_data['data']
            Latitude = form.cleaned_data['Latitude']
            Altitude = form.cleaned_data['Altitude']
            metodos = form.cleaned_data['metodos']
            if metodos == 'HS':
                  Tx = form.cleaned_data['Tx']
                  Tn = form.cleaned_data['Tn']
                  Tm = form.cleaned_data['Tm']
                  nome = "Hargreaves-Samani (1985)"
                  ETo = calcular_eto_HS_1985(Tm, Tx, Tn, Latitude,data)
            elif metodos=='PM':
                  Tx = form.cleaned_data['Tx']
                  Tn = form.cleaned_data['Tn']
                  Tm = form.cleaned_data['Tm']
                  UR = form.cleaned_data['UR']
                  vento = form.cleaned_data['vento']
                  Radglobal = form.cleaned_data['Radglobal']
                  nome ="Penman-Monteith - FAO56"
                  ETo = calcular_eto_pm_fao56(Tm, Tx, Tn, UR, vento, Radglobal, Latitude, Altitude,data)
            elif metodos=='HSJ':
                  Tx = form.cleaned_data['Tx']
                  Tn = form.cleaned_data['Tn']
                  Tm = form.cleaned_data['Tm']
                  vento = form.cleaned_data['vento']
                  nome = "Hargreaves-Samani modificado por Jensen et al. (1985)"
                  ETo = calcular_eto_HSJ_1997(Tm, Tx, Tn, vento, Latitude,data)
            else:
                  Tx = form.cleaned_data['Tx']
                  Tn = form.cleaned_data['Tn']
                  Tm = form.cleaned_data['Tm']
                  UR = form.cleaned_data['UR']
                  nome = "Hargreaves-Samani modificado por Lima Junior (1985)"
                  ETo = calcular_eto_HSJ_1997(Tm, Tx, Tn, UR, Latitude,data)
                 
                 
        resultado = ETo
        detalhe = nome
    else:
        resultado = 0.0
                  


    return render(request,'calETo/ETo.html',  {'form': form, 'detalhe': detalhe,'resultado':resultado,})
