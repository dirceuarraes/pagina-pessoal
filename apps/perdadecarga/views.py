from django.shortcuts import render
from apps.perdadecarga.forms import hfForms
from scripts.rotinas import calDarcyWeisbach, calHazenWilliams

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






def calhf(request):
    resultado = None
    detalhe = None
    form = hfForms()
    if request.method == 'POST':
        form = hfForms(request.POST)

        if form.is_valid():
            metodos=form.cleaned_data['metodos']
            material=form.cleaned_data['material']
            vazao=form.cleaned_data['vazao']/(1000.0*3600.0)
            comprimento=form.cleaned_data['comprimento']
            diametro=form.cleaned_data['diametro']
            F = 1.0
            if metodos == "DW":
                rugosidade = RUGOSIDADES[material]/1000
                nome = "Darcy-Weisbach"
                
                hf = calDarcyWeisbach(vazao, diametro, comprimento, rugosidade, F)
            else:
                Chw =CHW[material]
                nome = "Hazen-Wiliams"
                hf = calHazenWilliams(vazao, diametro, comprimento, Chw,F)
            
        resultado = hf
        detalhe = nome
    else:
        resultado = 0.0
        detalhe = "Erro"  

    

    

    return render(request, 'perdadecarga/calPerda.html', {'form': form, 'detalhe': detalhe, 'resultado':resultado,})