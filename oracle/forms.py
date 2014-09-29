from django import forms
from Test.models import system, Detail
from django.forms.widgets import *
from datetime import datetime


def get_my_choices():
	lista=[]
	for a in Detail.objects.filter(is_oracle=True):
		if a.test_id <= 7:
			lista.append((str(a.test_id),"Task 1a: Test batch 1, Week %s" %(a.test_id-1)))
		elif a.test_id <= 13:
			lista.append((str(a.test_id),"Task 1a: Test batch 2, Week %s" %(a.test_id-1-6))) 	
		elif a.test_id <= 19:
                        lista.append((str(a.test_id),"Task 1a:Test batch 3, Week %s" %(a.test_id-1-12)))
		else:
			lista.append((str(a.test_id),"Task 1a: Additional test batch 4, Week %s" %(a.test_id-1-18)))
	return tuple(lista)
def getJqueryChoices():
	return tuple([(x.test_id, x.test_id) for x in Detail.objects.all()])

def get_my_data():
        lista=[]
        for a in Detail.objects.filter(finished__lte=datetime.now()):
		
                if a.test_id == 1:
			lista.append((str(a.test_id),"Dry-run test of Task 1a"))
		elif a.test_id == -1:
			k=1
		elif a.test_id <= 7:
                        lista.append((str(a.test_id),"Task 1a: Test batch 1, Week %s" %(a.test_id-1)))
                elif a.test_id <= 13:
                        lista.append((str(a.test_id),"Task 1a: Test batch 2, Week %s" %(a.test_id-1-6)))
                elif a.test_id <= 19:
                        lista.append((str(a.test_id),"Task 1a: Test batch 3, Week %s" %(a.test_id-1-12)))
                elif a.test_id <= 40:
                        lista.append((str(a.test_id),"Task 1a: Additional test batch, Week %s" %(a.test_id-1-18)))
		elif a.test_id == 41:
			lista.append((str(a.test_id),"Dry-run test of Task 2a"))
		elif a.test_id <= 46:
			lista.append((str(a.test_id),"Task 2a: Test batch 1, Week %s" %(a.test_id-41)))
		elif a.test_id <= 51:
			lista.append((str(a.test_id),"Task 2a: Test batch 2, Week %s" %(a.test_id-46)))
		elif a.test_id <= 56:
			lista.append((str(a.test_id),"Task 2a: Test batch 3, Week %s" %(a.test_id-51)))
        return tuple(lista)

class getDataForm(forms.Form):
	testset=forms.ChoiceField(choices=get_my_choices())
	vectorized=forms.BooleanField(required=False, initial=False)
	def __init__(self, *args, **kwargs):
		super(getDataForm, self).__init__(*args, **kwargs)
		self.fields['testset'] = forms.ChoiceField(choices=get_my_data())

class OracleForm(forms.Form):
	docfile = forms.FileField(label='Select a file:', help_text='Select a file to upload that contains a JSON string with the answers of a test. The format of the JSON is described in the online guidelines of each task, e.g. <a href="/general_information/Task1a/"> here</a> for Task 1A')
	task=forms.ChoiceField(choices=(("1", "Task A"), 
("1ba", "Task B-Phase A"), ("1bb", "Task B-Phase B"),
),  help_text='Select the task you are submitting results for.')
	test=forms.ChoiceField(help_text='Specify the test set by choosing one from the drop down menu. Tests sets for task 1A, for example, can be downloaded from <a href="/Tasks/1A/"> here</a> and are those that been already used for the BioASQ challenge.')
	system_name=forms.ModelChoiceField(queryset=system.objects.all(),required=True,  help_text='Select one of your systems that will be used in the "Oracle Results" tab.')
	def __init__(self, *args, **kwargs):
	        super(OracleForm, self).__init__(*args, **kwargs)
        	self.fields['test'].choices= getJqueryChoices()
	
class OracleSelectVisibleForm(forms.Form):
	is_visible=forms.BooleanField(required=False, help_text="If enabled, your uploaded results will be visible in the oracle to any registered user. Otherwise, it will be visible only to you.", initial=True)
	keep_score=forms.BooleanField(required=False, help_text="If enabled, it will replace the previous score for the selected system and testset in the BioASQ database.", initial=True)
	hid=forms.CharField()
	#hid=forms.CharField(widget=forms.HiddenInput)


