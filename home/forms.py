from django import forms

# Create your forms here.
class ContactForm(forms.Form):
	full_name = forms.CharField(max_length = 100,widget=forms.TextInput())
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)