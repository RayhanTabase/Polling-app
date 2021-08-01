from django import forms
from .models import User

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    country_code = forms.CharField(max_length = 10)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    other_names = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    class Meta:
        model = User
        help_texts ={
            'username':None
        }
        fields =(
            "username",
            "first_name",
            "last_name",
            "other_names",
            "email",
            "phone_number",
            "profile_picture",
            "password",
            "date_of_birth"
        )
        
    def clean_password(self):
        password = self.cleaned_data["password"]
        # Password must be atleast 6 characters
        if len(password) > 5 : 
            return password
        raise forms.ValidationError("Password must be atleast 6 characters")
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        print(password,confirm_password)
        if confirm_password != password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password
    
    def clean_phone_number(self):
        country_code = self.cleaned_data.get("country_code")
        phone_number = self.cleaned_data.get("phone_number")
        # phone_number must be atleast 9 characters
        if len(phone_number) < 9 : 
            raise forms.ValidationError("phone number must be atleast 9 characters")
        user = User.objects.filter(country_code=country_code,phone_number=phone_number)
        if user:
            raise forms.ValidationError("phone number already exists")
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if len(first_name) < 2 :
            raise forms.ValidationError("First name must be atleast 2 characters")
        if len(first_name.split()) > 1 : 
            raise forms.ValidationError("First name must be only one word")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if len(last_name) < 2: 
            raise forms.ValidationError("Last name must be atleast 2 characters")
        if len(last_name.split()) > 1 : 
            raise forms.ValidationError("Last name must be only one word")
        return last_name
        
class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class':'form-control',  
    }))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_new_password(self):
        new_password = self.cleaned_data["new_password"]
        # Password must be atleast 6 characters
        if len(new_password) > 5 : 
            return new_password
        raise forms.ValidationError("Password must be atleast 6 characters")
    
    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if confirm_password != new_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

class EditProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    other_names = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    new_profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}),required=False)

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if len(first_name) < 2 :
            raise forms.ValidationError("First name must be atleast 2 characters")
        if len(first_name.split()) > 1 : 
            raise forms.ValidationError("First name must be only one word")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if len(last_name) < 2: 
            raise forms.ValidationError("Last name must be atleast 2 characters")
        if len(last_name.split()) > 1 : 
            raise forms.ValidationError("Last name must be only one word")
        return last_name
