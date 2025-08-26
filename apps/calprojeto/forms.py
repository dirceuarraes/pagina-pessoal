from django import forms

METODOSLL = (('DW',"Darcy-Weisbach"),
            ('HZ',"Hazen-Williams"),
            ('FL',"Flamant"),
            )

METODOSLDPS = (('DW',"Darcy-Weisbach"),
            ('HZ',"Hazen-Williams"),
            )

LINHASDOISSENTIDOS = [
    ('sim',"SIM"),
    ('nao',"NÃO"),
]

#Materiais de tubulações usando na irrigação
MATERIAIS_CHOICES = [
    ('AC', "Aço comercial (novo)"),
    ('AF', "Aço forjado (novo)"),
    ('AFO', "Aço forjado (oxidado)"),
    ('AG', "Aço galvanizado (novo)"),
    ('AGO', "Aço galvanizado (usado)"),
    ('PVC', "PVC"),
    ('PEAD', "Polietileno (PEAD)"),
    ('FE', "Ferro fundido (novo)"),
    ('FEO', "Ferro fundido (usado)"),
]

#Sistema de Irrigação
SISTEMA=[
    ('ILM',"MICROASPERSÃO"),
    ('ILG',"GOTEJAMENTO"),
    ('IAC',"ASPERSÃO CONVENCIONAL"),
]

       

class CalProjetoForms(forms.Form):
    #### Variaveis do sistema de irrigação #####
    sistema = forms.ChoiceField(
        label = "Sistema de Irrigação",
        choices=SISTEMA,
        widget=forms.Select
    ) 

    qemissor = forms.FloatField(
        label = "Vazão do emissor (L/h)",
        min_value = 0.5,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    PS = forms.FloatField(
        label = "Pressão de serviço do emissor (m) ",
        min_value = 0.5,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    Ee = forms.FloatField(
        label = "Espaçamento entre os emissores (m) ",
        min_value = 0.1,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    EL = forms.FloatField(
        label = "Espaçamento entre as Linhas Laterais (m) ",
        min_value = 0.1,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    AlturaEmissor = forms.FloatField(
        label = "Altura do emissor (m) ",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

         
    Qdisp = forms.FloatField(
        label = "Vazão disponível (L/h)",
        min_value = 1.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )  
       
    #Variaveis do Layout 
    #Linha Lateral

    materialLL = forms.ChoiceField(
        label = "Material da linha lateral",
        choices=MATERIAIS_CHOICES,
        widget=forms.Select
    )

    metodosLL = forms.ChoiceField(
        label = "Método Para o cálculo da Perda de Carga na Linha Lateral",
        choices=METODOSLL,
        widget=forms.Select
    )


    comprimentoLL = forms.FloatField(
        label = "Comprimento da linha  (m)",
        min_value=1.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    declividadeLL = forms.FloatField(
        label = "Declividade na direção da linha lateral (% positivo para aclive e negativo para declive)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )
   

    # Demais Linhas 

    #------------ Linha derrivação --------------------------------------
    materialLDPS = forms.ChoiceField(
        label = "Material da linha de Derivação, Principal e Sucção",
        choices=MATERIAIS_CHOICES,
        widget=forms.Select
    )

    metodosLDPS = forms.ChoiceField(
        label = "Método Para o cálculo da Perda de Carga nas demais Linhas",
        choices=METODOSLDPS,
        widget=forms.Select
    )

    comprimentoLD = forms.FloatField(
        label = "Comprimento da Linha de Derivação  (m)",
        min_value=1.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    linhasdoissentidos = forms.ChoiceField(
        label = "No layout tem linhas laterais nos dois sentidos do terreno",
        choices=LINHASDOISSENTIDOS,
        widget=forms.Select
    )

    declividadeLD = forms.FloatField(
        label = "Declividade na direção da linha de Derivação (% positivo para aclive e negativo para declive)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    #Linha principal

    comprimentoLP = forms.FloatField(
        label = "Comprimento da linha Principal  (m)",
        min_value=1.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    declividadeLP = forms.FloatField(
        label = "Declividade na direção da linha Principal (% positivo para aclive e negativo para declive)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    velocidademax = forms.FloatField(
        label = "Velocidade máxima na Linha Principal (m/s)",
        min_value=0.5,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    #Linha de Sucção

    comprimentoLS = forms.FloatField(
        label = "Comprimento da linha de Sucção  (m)",
        min_value=1.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    AlturaS = forms.FloatField(
        label = "Altura de Sucção (m)",
        min_value=0.5,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    #Perda de carga localizada
    Fator = forms.FloatField(
        label = "Porcentagem de perdas de carga localizadas no sistema (%)",
        min_value=0.5,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )







   

    