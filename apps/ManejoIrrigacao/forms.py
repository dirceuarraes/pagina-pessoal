from django import forms
from apps.culturas.models import Cultura
from apps.solos.models import Solo

FaseCultura = [('FI',"Inicial"),
            ('FM',"Média"),
            ('FF',"Final"),
]
SISTEMA=[
    ('ILM',"MICROASPERSÃO"),
    ('ILG',"GOTEJAMENTO"),
    ('IAC',"ASPERSÃO CONVENCIONAL"),
]


class CalManejoForm(forms.Form):
    
    cultura = forms.ModelChoiceField(
        label="Cultura",
        queryset=Cultura.objects.all(),  # Busca todas as culturas do banco
        widget=forms.Select(attrs={"class":"form-control"})
    )

    solo = forms.ModelChoiceField(
        label="Solo",
        queryset=Solo.objects.all(),
        widget=forms.Select(attrs={"class":"form-control"})
    )

    fase = forms.ChoiceField(
        label="Fase da Cultura",
        choices=FaseCultura,
        widget=forms.Select(attrs={"class":"form-control"})
    )

    sistema = forms.ChoiceField(
        label = "Sistema de Irrigação",
        choices=SISTEMA,
        widget=forms.Select(attrs={"class":"form-control"})
    ) 

    VazaoEmissor = forms.FloatField(
        label = "Vazão do Emissor (L/h)",
        min_value = 0.1,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    espacamentoEmissor = forms.FloatField(
        label = "Espaçamento entre Emissores (m)",
        min_value = 0.1,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    espacamentoLinha = forms.FloatField(
        label = "Espaçamento entre Linhas (m)",
        min_value = 0.1,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    raiomolhado = forms.FloatField(
        label = "Raio molhado (m)",
        min_value = 0.1,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )      

    eficIrrigacao = forms.FloatField(
        label = "Eficiência da Irrigação (%)",
        min_value = 10,
        max_value = 100,
        initial = 85,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    Uatual = forms.FloatField(
        label = "Umidade Atual à Base de Massa (g/g)",
        min_value = 0.1,
        max_value = 1,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    
    