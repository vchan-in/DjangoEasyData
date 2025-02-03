from django import forms
from .models import UsersDetails
 
 
# creating a form
class UserDetailForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = UsersDetails
 
        # specify fields to be used
        fields = [
            "name",
            "gender",
            "email",
            "phone",
            "credit_card",
            "username",
            "password",
        ]