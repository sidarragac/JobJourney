from django import forms

class RoadmapCharacteristics(forms.Form):
    interest = forms.CharField(label='Interest', max_length=100, required=True)
    objective = forms.CharField(label='Objective', max_length=100, required=True)
    salary = forms.FloatField(label='Salary', min_value=0.0, required=False)