from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Profile
from django.forms.fields import CharField


# Create your forms here.

class NewUserForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'User Name'}), required=True, label='Username')
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}),required=True, label='Email')
	# first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}),required=True, label='First Name')
	# last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}),required=True, label='Last Name')
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),required=True, label='Password')
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),required=True, label='Password')


	class Meta:
		model = User
		fields = ('username','email','password1','password2')

		def save(self, commit=True):
			user = super(NewUserForm, self).save(commit=False)
			user = self.cleaned_data['email']
			if commit:
				user.save()
			return user
    
USER_STATUS = (
    # ('not_set', 'not_set'),
    ('talent','talent'),
    ('startup','startup')
)
class profileForm(forms.ModelForm):
    user_type = forms.ChoiceField( choices=USER_STATUS, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('user_type',)
        # exclude = ('user', 'image')