from django.contrib.auth.forms import UserCreationForm, forms
from food.models import SiteUser 

class SiteUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = SiteUser 
        fields = UserCreationForm.Meta.fields + ('username','email','phone_number','first_name','last_name')
        #labels = {
        #    'phone_number':'9********'
        #}
        widgets = {
            'phone_number': forms.TextInput()
        }