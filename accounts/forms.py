from django import forms
from .models import Account, UserProfile # import Account and UserProfile models

# -- Class Form for Register -- #
class RegistrationForm(forms.ModelForm):
    
    # -- field Enter Password for form -- #
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    
     # -- field Confirm Password for form -- #
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))
      
    class Meta:
        model = Account # model inherit Account model
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password'] # add some field from Account model

    # -- add CSS, Boostraps for all field -- #
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        # add for each fields #
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name' 
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Addess'
        
        # add all field
        for field in self.fields: 
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    # -- Function to check and confirm password -- #
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password: # raise error
            raise forms.ValidationError(
                "Passowrd does not match."
            )
            

# -- Create a User Form to edit fields in Account model -- #
class UserForm(forms.ModelForm):
    
    class Meta:
        
        model = Account
        
        fields = ['first_name', 'last_name', 'phone_number']
        
    # -- add CSS, Boostraps for all field -- #
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        # add all field
        for field in self.fields: 
            self.fields[field].widget.attrs['class'] = 'form-control'

        
# -- Create a User Profile Form to edit fields in UserProfile model -- #        
class UserProfileForm(forms.ModelForm):
    
    
    profile_picture = forms.ImageField(required=False, error_messages={"invalid": ('Image files only')}, widget=forms.FileInput)
    
    class Meta:
        
        model = UserProfile
        
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']
        
        
    # -- add CSS, Boostraps for all field -- #
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        # add all field
        for field in self.fields: 
            self.fields[field].widget.attrs['class'] = 'form-control'