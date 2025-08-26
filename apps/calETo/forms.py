from django import forms

METODOS = (('HS',"Hargreaves-Samani (1985)"),
            ('PM',"Penman-Monteith - FAO56"),
            ('HSJ',"Hargreaves-Samani mod Jensen et al. (1997)"),
            ('HSLJ',"Hargreaves-Samani mod Lima Junior (2022)"),
          )
        

class EToForms(forms.Form):

    

    data = forms.DateField(
        label = "Data",
        widget=forms.DateInput(attrs={"type":"date","class":"form-control"})
    )

    metodos = forms.ChoiceField(
        label = "Métodos",
        choices=METODOS,
        widget=forms.Select
    )

    Latitude = forms.FloatField(
        label = "Latitude (em graus e negativo para hemisfério sul)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    Altitude = forms.FloatField(
        label = "Altitude (metros)",
        min_value = 0.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )


    Tx = forms.FloatField(
        label = "Temperatura máxima (°C)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    Tn = forms.FloatField(
        label = "Temperatura mínima (°C)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    Tm = forms.FloatField(
        label = "Temperatura média (°C)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    vento = forms.FloatField(
        label = "Velocidade do Vento (m/s)",
        min_value = 0.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    UR = forms.FloatField(
        label = "Umidade Relativa - UR(%)",
        min_value = 0.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    Radglobal = forms.FloatField(
        label = "Radiação Global - Rg(MJ/m² dia)",
        min_value = 0.0,        
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

