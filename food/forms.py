from django.contrib.auth.forms import UserCreationForm, forms
from food.models import SiteUser 

class SiteUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150,help_text='یوزرنیمت')
    class Meta(UserCreationForm.Meta):
        model = SiteUser 
        fields = UserCreationForm.Meta.fields + ('username','email','phone_number','first_name','last_name')
    
        widgets = {
            'phone_number': forms.TextInput()
        }
        help_text = {
            'username': 'یوزرت ',
            'password1': 'اوووووو'
        }
        label={'username':'یوزرنیم',
        'password1': 'اوووووو'}

class DepositForm(forms.Form):
    deposit = forms.IntegerField(min_value=5000,max_value=10000000,
                                error_messages={'required':'لطفا عدد را وارد کنید'
                                                ,'invalid':"مقدار داده شده صحیح نم باشد"
                                                ,'min_value':'حداقل مقدار ورودی باید ۵۰۰۰ باشد'
                                                ,'max_value':'حداکثر مقدار ورودی باید ۱۰۰۰۰۰۰ باشد'})


class WithdrawForm(forms.Form):
    withdraw = forms.IntegerField(min_value=5000,max_value=10000000,
                                error_messages={'required':'لطفا عدد را وارد کنید'
                                                ,'invalid':"مقدار داده شده صحیح نم باشد"
                                                ,'min_value':'حداقل مقدار ورودی باید ۵۰۰۰ باشد'
                                                ,'max_value':'حداکثر مقدار ورودی باید ۱۰۰۰۰۰۰ باشد'})




