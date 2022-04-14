from django import forms

from bereket.models import Client, Product, Consumption


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
            'class': 'u-form-group u-form-name u-border-1 u-border-grey-30 u-input u-input-rectangle u-white',
            'placeholder': 'Логин'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
            'class': 'u-form-group u-form-name u-border-1 u-border-grey-30 u-input u-input-rectangle u-white',
            'placeholder': 'Пароль'}))


class ClientForm(forms.ModelForm):
    name = forms.CharField(label='', max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
        }))
    surname = forms.CharField(label='', max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-2',
        }))
    lastname = forms.CharField(label='', max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-3',
        }))
    passport_id = forms.CharField(label='', max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-4',
        }))

    validity = forms.DateField(widget = forms.SelectDateWidget)
    who_gave = forms.CharField(label='', max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-6',
       }))
    phone_number = forms.CharField(label='', max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-6',
       }))

    class Meta:
        model = Client
        fields = ["name", "surname", "lastname", "passport_id", "validity", "who_gave", "phone_number"]


class SaleForm(forms.Form):
    first_payment = forms.IntegerField(label='', required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
    }))
    price = forms.IntegerField(label='', required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
    }))


class TransactionForm(forms.Form):
    payment = forms.IntegerField(label='Взнос', required=True, widget=forms.TextInput(attrs={
        'class': 'u-form-group u-form-name u-label-left u-label u-border-1 u-border-grey-30 u-input u-input-rectangle',
    }))


class CashForm(forms.Form):
    price = forms.IntegerField(label='', required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
    }))


class ConsumptionForm(forms.ModelForm):
    who_got = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
    }))
    summa = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
    }))
    reason = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white u-input-1',
    }))

    class Meta:
        model = Consumption
        fields = ["who_got", "summa", "reason"]


class ProductForm(forms.ModelForm):
    number = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle',
    }))
    name = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle',
    }))
    price = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle',
    }))
    amount = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle',
    }))

    class Meta:
        model = Product
        fields = ('number', 'name', 'price', 'amount')