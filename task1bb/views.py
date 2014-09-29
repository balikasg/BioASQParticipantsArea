# Create your views here.
from django.core.files import File
from Test.models import *
from models import *
from task1b.models import *
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import json, subprocess, os
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from uploads.forms import DocumentForm
from os import listdir

@login_required
def download_test1bb(request, distro):
	try:
		distro=int(distro)
		target=Detail1b.objects.filter(started__lte=datetime.now()).filter(phase="B").get(test_id=distro)
	except:
		user=request.user
		dictionary=createPage(user)
		dictionary['errors']=["The test you requested is not currently active.\n"]
		return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
	path=target.path
	target.number_of_downloads+=1
	downs=json.loads(target.downloaders)
        downs.append(str(request.user.username))
        target.downloaders=json.dumps(downs)
	target.save()
	wrapper = FileWrapper( open( path, "r" ) )
	response=HttpResponse(wrapper, content_type="text/plain")
	filename="attachment; filename=BioASQ-task2bPhaseB-testset%d" %(target.test_id-3)
	response['Content-Disposition'] =filename
	return response

def createPage(user):
	"""Given the logged in user returns the active testset, attempts of the user, released testsets and initializes a form."""
	active=Detail1b.objects.filter(phase="B").filter(finished__gte=datetime.now()).filter(started__lte=datetime.now())
        attempts=[item for item in user_results_1bb.objects.all() if item.user == User.objects.get(username=user) and item.test_id in [x for x in Detail1b.objects.filter(phase="B").filter(test_id__gte=4)]]
        if active:
                active=active[0]
        else:
                active=None
        tests=Detail1b.objects.filter(phase="B").filter(test_id__gte=4).filter(started__lte=datetime.now())
        form = DocumentForm()
        form.fields['system_name'].queryset=system.objects.filter(user=user)
        return {"tests":tests, "current_test":active, "attempts":attempts, "form":form}


#Code for downloading the test sets of Phase A from the API
@csrf_exempt
def Task1bbRemote(request, pk):
        #Make some checks about pk
	if request.method=="POST":
		try:
			data=json.loads(request.raw_post_data)
			username=data['username']
			password=data['password']
			pk=int(pk)
		except:
			return HttpResponse("Error with the format of the json you posted. \n")
		user = authenticate(username=username, password=password)
		if user is None:
			return HttpResponse("Error with the credentials you posted in the JSON. Check your username and your password. \n")
		if user.is_active:
			try:
				target=Detail1b.objects.filter(started__lte=datetime.now()).filter(phase="B").get(test_id=(pk+3))
			except:
				return HttpResponse("The test set number you have put in the URL caused an error. Please check and try again. \n")
			path=target.path
			target.number_of_downloads+=1
			downs=json.loads(target.downloaders)
		        downs.append(str(user.username))
		        target.downloaders=json.dumps(downs)
			target.save()
			wrapper = FileWrapper( open( path, "r" ) )
			response=HttpResponse(wrapper, content_type="text/plain")
			filename="attachment; filename=BioASQ-task2bPhaseB-testset%d" %(target.test_id-3)
			response['Content-Disposition'] =filename
			return response
		else:
			return HttpResponse("Your account is not active. Please click on the activation link or contact the administrations.\n")


@login_required
def download_results_1bb(request, ts, s):
	dictionary=createPage(request.user)
        try:
                sys=system.objects.filter(user=request.user).get(system=s)
        except:
		dictionary["errors"]=["You are trying to download results for a system that doesn't belong to you!"]
                return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
        try:
                test=Detail1b.objects.filter(phase="B").get(test_id=ts)
        except:
		dictionary["errors"]=["You are trying to download results for a testset that doesn't exist"]
                return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
        p=user_results_1bb.objects.filter(test_id=test).filter(system=sys)
        if p:
                path=p[0].path
                wrapper = FileWrapper( open( path ) )
                response=HttpResponse(wrapper, content_type="application/txt")
                response['Content-Disposition'] ='attachment; filename="results_2b_phaseB.json" '
                return response
        else:
		dictionary['errors']=["You have not submitted results for this system and testset"]
                return render_to_response("Task1B-B.html", dictionary, RequestContext(request))








@login_required
def Task1bPhaseBSubmitWebInterface(request):
	user=request.user
	dictionary=createPage(user) #Given the logged in user returns the active testset, attempts of the user, released testsets and initializes a form.
	errors=[]
	if request.method=='POST': #If the user submits data...
		form = DocumentForm(request.POST, request.FILES)
		form.fields['system_name'].queryset=system.objects.filter(user=request.user)
		if form.is_valid():
			c=form.cleaned_data
			systems=system.objects.get(system=c['system_name'])
			try: 
				user_data=json.loads(request.FILES['docfile'].read())
			except:
				dictionary['errors']=["Error while decoding the JSON"]
				return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
			#Having the valid user JSON make whatever checks you want	
			test_ids=[]
		        active=Detail1b.objects.filter(phase="B").filter(finished__gte=datetime.now()).filter(started__lte=datetime.now())
			actives=golden_question_1b.objects.filter(testset=Detail1b.objects.filter(phase="A").filter(test_id=active[0].test_id))
			#actives=golden_question_1b.objects.filter(testset=Detail1b.objects.filter(phase="A")).filter(question_id=active[0].test_id)

			for question in actives:
				test_ids.append(question.question_id)
			#Check that the user submits data for every question
			if not len(user_data['questions'])==active[0].number_of_questions:
				dictionary['errors']=["Error! The number of the questions in the JSON is different from the number of questions in the active test set."]
				return render_to_response("Task1B-B.html", dictionary, RequestContext(request))	
			for question in user_data['questions']:
				#Check that the PMIDs submitted belong to active PMIDs
				try: 
					if not question['id'] in test_ids:
						dictionary['errors']=["Error! Question id: %s. The question id doesn't belong to the active test set." %question['id']] 
						return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
				except:
					dictionary['errors']=["Error! Question id not found. Please make sure you submit the correct JSON format."]
					return render_to_response("Task1B-B.html", dictionary, RequestContext(request))		
				if not (("exact_answer" in question) or ("ideal_answer" in question)):
					dictionary['errors']=["Error! Question id: %s. No exact or ideal answer for this question." %question['id']]
                                        return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
				#Factoid Questions: a maximum of 5 entities
				if golden_question_1b.objects.get(question_id=question['id']).type=="factoid":
					try: 
						if len(question['exact_answer'])>5:
							dictionary['errors']=["Error! Question id: %s. In the exact answer of this factoid question there are more than 5 entity names, which is not allowed." %question['id']]
							return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
					except:
						pass		
				#List question: 100 elements of 100 characters each
				if golden_question_1b.objects.get(question_id=question['id']).type=="list":
					try:
						if len(question['exact_answer'])>100:
							dictionary['errors']=["Error! Question id: %s. In the exact answer of this list question there are more than 100 elements, which is not allowed." %question['id']]
							return render_to_response("Task1B-B.html", dictionary, RequestContext(request))	
						for item in question['exact_answer']:
							for inner_item in item:
								if len(inner_item)>400:
									dictionary['errors']=["Error! Question id: %s. In the exact answer of this list question the element %s has more than 100 characters, which is not allowed." %(question['id'], inner_item)]
									return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
					except:
						pass				
				#Yes/no question stricktly "yes" or "no" answer
				if golden_question_1b.objects.get(question_id=question['id']).type=="yesno":
					try:
						if not (question['exact_answer']=="yes" or question['exact_answer']=="no"):
							dictionary['errors']=["Error! Question id: %s. In the exact answer of this yes/no question the answer should be either 'yes' or 'no'. Note that there are no capitals or punctuation." %question['id']]
							return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
					except:
						pass
				try:
					if len(question['ideal_answer'].split())>350:
						dictionary['errors']=["Error! Question id: %s. In the ideal answer of this question the words are more than 200" %question['id']]
						return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
				except:
					pass					
					
			#Having checked everything save the file.
			pt="/home/bioasq/public_html/webexample/uploads/users/task2b/phaseB/testset%d/%s.json" %(active[0].test_id, systems.system)
			try:
				f=open(pt, 'w')
				myfile=File(f)
				print>>myfile, json.dumps(user_data)
				myfile.close()
			except:
				dictionary['errors']=["Error while saving the file. Try again later."]
				return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
			#Delete previous uploads for the same user, system, testset and update the database with information for the saved file
			entry2=user_results_1bb.objects.filter(system=systems).filter(test_id=active[0]).delete()	
			entry2=user_results_1bb(system=systems, user=user, test_id=active[0], path=pt).save()
			dictionary['errors']=["Results saved successfully!"]
			dictionary['attempts']=[item for item in user_results_1bb.objects.all() if item.user == User.objects.get(username='bioasq') and item.test_id in [x for x in Detail1b.objects.filter(phase="B").filter(test_id__gte=4)]]
			return render_to_response("Task1B-B.html", dictionary, RequestContext(request))
	return render_to_response("Task1B-B.html", dictionary, RequestContext(request))




@csrf_exempt
def Task1bPhaseBSubmitApi(request, pk):
	if request.method=='POST':
		active=Detail1b.objects.filter(phase="B").filter(finished__gte=datetime.now())
		if active:
			active=active[0]
		else:
			return HttpResponse("Currently, there is no test set active for Task1B-Phase B, in order to upload your results!\n")
		try:
			distro=int(pk)+3
		except:
			return HttpResponse("Error: The integer that corresponds to the active test set in the URI caused an error. Check the URI format.\n")
		if not active.test_id==distro:
			return HttpResponse("Error: The test id you provided in the URI doesn't match the currently active test id. Check the test id and try again. \n")		
		try:
			data_raw=request.raw_post_data
			user_data=json.loads(data_raw)
		except:
			return HttpResponse("Error during decoding JSON. Valid JSON object?\n")
		user=authenticate(username=user_data['username'], password=user_data['password'])	
		if user is None:
			return HttpResponse("There was a problem during your authentication. Please, check your username and your password! \n")
		if not user.is_active:
			return HttpResponse("Your account is not active. Please click on the activation link you have received in your mail account or contact the administrators.\n")	
		try:	
			systems=system.objects.filter(user=user).get(system=user_data["system"])
		except:
			return HttpResponse("The system name you provided in the JSON does not belong to you or does not exist. Check the its name and try again!\n")
			
		#Having the valid user JSON make whatever checks you want	
		test_ids=[]
		actives=golden_question_1b.objects.filter(testset=Detail1b.objects.filter(phase="A").get(test_id=active.test_id))
		for question in actives:
			test_ids.append(question.question_id)
		#Check that the user submits data for every question
		if not len(user_data['questions'])==active.number_of_questions:
			return HttpResponse("Error! The number of the questions in the JSON is different from the number of questions in the active test set.\n")	
		for question in user_data['questions']:
			#Check that the PMIDs submitted belong to active PMIDs
			try: 
				if not question['id'] in test_ids:
					return HttpResponse("Error! Question id: %s. The question id doesn't belong to the active test set.\n" %question['id']) 
			except:
				return HttpResponse("Error! Question id not found. Please make sure you submit the correct JSON format.\n")			
			if not (("exact_answer" in question) or ("ideal_answer" in question)):
                                        HttpResponse("Error! Question id: %s. No exact or ideal answer for this question." %question['id'])
			#Factoid Questions: a maximum of 5 entities
			
			if golden_question_1b.objects.get(question_id=question['id']).type=="factoid":
				try: 
					if len(question['exact_answer'])>5:
						return HttpResponse("Error! Question id: %s. In the exact answer of this factoid question there are more than 5 entity names, which is not allowed.\n" %question['id'])
				except:
					pass		
			#List question: 100 elements of 100 characters each
			if golden_question_1b.objects.get(question_id=question['id']).type=="list":
				try:
					if len(question['exact_answer'])>100:
						return HttpResponse("Error! Question id: %s. In the exact answer of this list question there are more than 100 elements, which is not allowed.\n" %question['id'])	
					for item in question['exact_answer']:
						for inner_item in item:
							if len(inner_item)>400:
								return HttpResponse("Error! Question id: %s. In the exact answer of this list question the element %s has more than 100 characters, which is not allowed.\n" %(question['id'], inner_item))
				except:
					pass				
			#Yes/no question stricktly "yes" or "no" answer
			if golden_question_1b.objects.get(question_id=question['id']).type=="yesno":
				try:
					if not (question['exact_answer']=="yes" or question['exact_answer']=="no"):
						return HttpResponse("Error! Question id: %s. In the exact answer of this yes/no question the answer should be either 'yes' or 'no'. Note that there are no capitals or punctuation.\n" %question['id'])
						
				except:
					pass
			try:
				if len(question['ideal_answer'].split())>200:
					return HttpResponse("Error! Question id: %s. In the ideal answer of this question the words are more than 200\n" %question['id'])
			except:
				pass
		#Having checked everything save the file.
		pt="/home/bioasq/public_html/webexample/uploads/users/task2b/phaseB/testset%d/%s.json" %(active.test_id, systems.system)
		try:
			f=open(pt, 'w')
			myfile=File(f)
			print>>myfile, data_raw
			myfile.close()
		except:
			return HttpResponse("Error while saving the file. Try again later.\n")
		#Delete previous uploads for the same user, system, testset and update the database with information for the saved file
		entry2=user_results_1bb.objects.filter(system=systems).filter(test_id=active).delete()	
		entry2=user_results_1bb(system=systems, user=user, test_id=active, path=pt).save()
		return HttpResponse("Results saved successfully!\n")
	else:
		return HttpResponse("You need to use the 'POST' method in your Http Request.\n")



def evaluate1bb(request):
	s=""
        for test in Detail1b.objects.filter(phase="B").filter(test_id__gte=4):
		if not test.is_oracle:
			for participant in user_results_1bb.objects.filter(test_id=test):
				evaluation_measures_1bb.objects.filter(system=participant.system).filter(testset=test).delete()
				e=evaluation_measures_1bb(testset= test, system=participant.system, acc=-1, s_acc=-1, l_acc=-1, mrr=-1, prec=-1, rec=-1, fmeas=-1, r2p=-1, r2r=-1, r2f=-1, r4p=-1, r4r=-1, r4f=-1).save()		
		else:
			#gold_results=test.golden_path#Changed when we took the golden results for the second year
			gold_results='/home/bioasq/public_html/webexample/task1b/golden_files/golden2ndyear.json'
                        for participant in user_results_1bb.objects.filter(test_id=test):
                                system_results=participant.path
				a,b=eval1bbb(gold_results, system_results)
				s+=participant.system.system_description+" "+", ".join(b)+"\r\n"
                                evaluation_measures_1bb.objects.filter(system=participant.system).filter(testset=test).delete()
				try:
					s+=", ".join(a)+"\n"
					e=evaluation_measures_1bb(testset=test, system=participant.system, acc=float(a[0]), s_acc=float(a[1]), l_acc=float(a[2]), mrr=float(a[3]), prec=float(a[4]), rec=float(a[5]), fmeas=float(a[6]), r2p=float(b[0]), r2r=float(b[1]), r2f=float(b[2]), r4p=float(b[3]), r4r=float(b[4]), r4f=float(b[5]), read=-1, recall=-1, rep=-1, preci=-1).save()
				except:
					pass
					e=evaluation_measures_1bb(testset=test, system=participant.system, acc=0, s_acc=0, l_acc=0, mrr=0, prec=0, rec=0, fmeas=0, r2p=float(b[0]), r2r=float(b[1]), r2f=float(b[2]), r4p=float(b[3]), r4r=float(b[4]), r4f=float(b[5]), read=-1, recall=-1, rep=-1, preci=-1).save()
				
        return HttpResponse(s)
	


def eval1bbb(goldenPath, testPath):
        com='java -cp $CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar evaluation.EvaluatorTask1b -phaseB  {0} {1} /home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/PMCdocslist.txt'.format(goldenPath, testPath)
        result=subprocess.Popen(com.split(),  stdout=subprocess.PIPE)
        p=result.communicate()
        c=p[0].split()
        com='python /home/bioasq/public_html/webexample/task1bb/rouge-bioasq/rouge.py {0} {1}'.format(goldenPath, testPath)
        proc = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return c, out[1:-2].split(', ')


















def results1bb(request):
        tests=Detail1b.objects.filter(phase="B").filter(test_id__gte=1).filter(test_id__lte=3)
        evaluation=evaluation_measures_1bb.objects.all()
        return render_to_response('results1bb.html', {"tests":tests, "evaluation":evaluation }, RequestContext(request))

def results2bb(request):
        tests=Detail1b.objects.filter(phase="B").filter(test_id__gte=4)
        evaluation=evaluation_measures_1bb.objects.filter(testset__gte=4)
        return render_to_response('results2bb.html', {"tests":tests, "evaluation":evaluation }, RequestContext(request))

















