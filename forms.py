from django import forms
from django.forms.widgets import *
#from captcha.fields import CaptchaField
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from Test.models import user_profile, Detail, system
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _


class sendMessage(forms.Form):
	sender=forms.CharField(max_length=100, initial="admin@bioasq.org")
        subject=forms.CharField(max_length=100, initial="[BioASQ]")
	message=forms.CharField(widget=forms.Textarea, max_length= 3000, initial="Dear Participants,")

class UserRegForm(RegistrationFormUniqueEmail):
	institution=forms.CharField(max_length=200)
	task1a=forms.BooleanField(required=False, initial=True)
	task1b1=forms.BooleanField(required=False, initial=True)
	task1b2=forms.BooleanField(required=False, initial=True)
	task2a=forms.BooleanField(required=False, initial=True)
	task2b=forms.BooleanField(required=False, initial=True)
	receive_information=forms.BooleanField(required=False, initial=True)



last=[int(a.test_id) for a in Detail.objects.all()]
last=max(last)+1
class createTestForm(forms.Form):
	starting_date=forms.CharField(max_length= 30, label="From what date should I start selecting articles:", initial="2013/04/01")
	test_id=forms.IntegerField(label="Test Id:", initial=last)
	#abstracts=forms.IntegerField(label="Abstracts:")
	started=forms.DateTimeField(initial=datetime.date.today()+datetime.timedelta(days=1), label='Active from:')
	finished=forms.DateTimeField(label='Active until:', initial=(datetime.date.today()+datetime.timedelta(days=2)))

	
	
class createDataForm(forms.Form):
	starting_date=forms.CharField(label="Starting Date:")
	finishing_date=forms.CharField(label="Finishing Date:")
	abstracts=forms.IntegerField(label="Maximum Abstracts")
	
	
class ContactForm(forms.Form):
	name=forms.CharField()
	email=forms.EmailField()
	topic=forms.CharField()
	message=forms.CharField(widget=Textarea())	
	#captcha = CaptchaField()
	
class email_change_form(ModelForm):
	class Meta:
		model=User
		fields=('email', )


		
class add_system(forms.Form):
	system_name=forms.CharField(max_length=20)		
	system_description=forms.CharField(max_length=20)	
class task_selection_edit_form(ModelForm):
	class Meta:
		model=user_profile
		fields=('task1a', 'task1b1', 'task1b2', 'task2a','task2b','receive_information',)
	
		
		




