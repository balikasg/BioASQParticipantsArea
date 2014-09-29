from django import forms
from Test.models import*

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file:',
        help_text=''
    )
    system_name=forms.ModelChoiceField(queryset=system.objects.all())
    
   #def __init__(self, *args, *kwargs):
	   #accountid=kwargs.pop('username', None)
	   #super(DocumentForm, self).__init__(*args, **kwargs)
	   #
	   #if accountid:
		   #self.fields[]
