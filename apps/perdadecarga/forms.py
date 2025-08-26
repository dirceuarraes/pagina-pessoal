from django import forms


METODOS = (('DW',"Darcy-Weisbach"),
            ('HZ',"Hazen-Williams"),
            )


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

       

class hfForms(forms.Form):
  
       

    metodos = forms.ChoiceField(
        label = "Métodos",
        choices=METODOS,
        widget=forms.Select
    )

    material = forms.ChoiceField(
        label = "Material",
        choices=MATERIAIS_CHOICES,
        widget=forms.Select
    )

    comprimento = forms.FloatField(
        label = "Comprimento da tubulação (m)",
        min_value=0.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    diametro = forms.FloatField(
        label = "Diâmetro (mm)",
        min_value = 0.0,
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )


    vazao = forms.FloatField(
        label = "Vazão (L/h)",
        widget=forms.NumberInput(attrs={"classe":"form-control"})
    )

    