from django import forms
from .models import Poll, Candidate

class PollForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    closing_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))

    class Meta:
        model = Poll
        fields = ('name','image','closing_date','restrictionType','live_results')

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Title"

class CandidateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    party = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}),required=False)

    class Meta:
        model = Candidate
        fields= "__all__"
        exclude=['poll','categories_contesting']

class EditPollForm(forms.Form):
    name = forms.CharField()
    image = forms.ImageField(required=False)
    restrictionType = forms.CharField()
    closing_date = forms.DateField()
    live_results = forms.BooleanField(required=False)

class KeyForm(forms.Form):
    key = forms.CharField()
