from django import forms
class PredictionForm(forms.Form):
    speed = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'id': 'spped_id', 'class': 'pre', 'placeholder': '   Enter the Speed Of the Wind'}))
    therotic= forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'id': 'therotic_id', 'class': 'pre', 'placeholder': '  Enter the Theoretical_Power_Curve Value'}))
    direction = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'id': 'direction_id', 'class': 'pre', 'placeholder': '    Enter the Wind Direction value'}))
