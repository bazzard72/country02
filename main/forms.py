from django import forms
from main.models import Country, Review

class CreateCountryForm(forms.ModelForm):
	class Meta:
		model = Country 
		fields = '__all__'
		#exclude = ('flag',)

class CreateUserForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30,widget=forms.PasswordInput())
	email = forms.EmailField(required=False)

class SigninForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30,widget=forms.PasswordInput())
	
class CreateReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		exclude = ('date','country','user') 

class EditReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		exclude = ('date','country','user')
		#fields = 'content'