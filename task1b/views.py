# Create your views here.
from django.core.files import File
from Test.models import *
from models import *
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import json, subprocess
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from uploads.forms import DocumentForm
import os, csv

@login_required
def download_resources(request):
        the_file = '/home/bioasq/public_html/webexample/BioASQ-Resources-Services-taskB.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response



def results1b(request):
	tests=Detail1b.objects.filter(phase="A").filter(test_id__gte=1).filter(test_id__lte=3)
	evaluation=evaluation_measures_1b.objects.all()
	return render_to_response('results1ba.html', {"tests":tests, "evaluation":evaluation }, RequestContext(request))


def results2b(request):
        tests=Detail1b.objects.filter(phase="A").filter(test_id__gte=4)
        evaluation=evaluation_measures_1b.objects.filter(testset__gte=4)
        return render_to_response('results2ba.html', {"tests":tests, "evaluation":evaluation }, RequestContext(request))



login_required
def task1b_dry(request):
        the_file = '/home/bioasq/public_html/webexample/task1b/testfiles/dry-run.json'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


@login_required
def task1bb_dry(request):
        the_file = '/home/bioasq/public_html/webexample/task1bb/testfiles/dry-run.json'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response



#Code for downloading the tests from the Web Interface
#You take the distro from the URL and you ask the database for the path.
#You return the file to the user.
#REQUIRES every test set in a file
@login_required
def download_test1ba(request, distro):
        errors=[]
	try:
	        target=Detail1b.objects.filter(phase="A").get(test_id=distro)
        	path=target.path
	        target.number_of_downloads+=1
		downs=json.loads(target.downloaders)
		downs.append(str(request.user.username))
		target.downloaders=json.dumps(downs)
	        target.save()
	except:
		return HttpResponse("Error 500.\nThe test set you have asked is not available!")
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        if target.test_id==0:
		response['Content-Disposition'] ='attachment; filename="development_set.json"'
	else:
		filename="attachment; filename=BioASQ-task2bPhaseA-testset%d" %(target.test_id-3)
		response['Content-Disposition'] =filename
        return response


#Code for downloading the test sets of Phase A from the API
@csrf_exempt
def Task1baRemote(request, pk):
	if request.method=="POST":
		try:
			data=json.loads(request.raw_post_data)
			username=data['username']
			password=data['password']
		except:
			return HttpResponse("Error with the format of the json you posted. \nCheck you have submitted a valid JSON and you have added you username and your password.\n")
		user = authenticate(username=username, password=password)
		if user is None:
			return HttpResponse("Error with the credentials you posted in the JSON. They are not valid.\nCheck your username and your password. \n")	
		if user.is_active:
			try: 
				pk=int(pk)
				target=Detail1b.objects.filter(phase="A").get(test_id=pk+3)
			except:
				return HttpResponse("The test set number you have put in the URL caused an error. Please check and try again. \n")	
			try:
				path=target.path
				target.number_of_downloads+=1
				downs=json.loads(target.downloaders)
	                        downs.append(str(user.username))
	                        target.downloaders=json.dumps(downs)
				target.save()
			except:
				return HttpResponse("The test set you have asked is not available yet. Please check and try again. \n")
			wrapper = FileWrapper( open( path, "r" ) )
			response=HttpResponse(wrapper, content_type="text/plain")
			response['Content-Disposition'] ='attachment; filename="BioASQ-task2bPhaseA-testset%d" %(target.test_id-3)'
			return response
		else:
			return HttpResponse("Your account is not active. Please click on the activation link or contact the administrations.\n")

@login_required
def download_results_1b(request, ts, s):
	try:
		sys=system.objects.filter(user=request.user).get(system=s)
	except:
		return render_to_response("Task1B-A.html", {"errors":"No System"}, RequestContext(request))
	try:
		test=Detail1b.objects.filter(phase="A").get(test_id=int(ts[0]))
	except:
		return render_to_response("Task1B-A.html", {"errors":"No Detail"}, RequestContext(request))
	p=user_results_1b.objects.filter(test_id=test).filter(system=sys)
	if p:
		path=p[0].path
		wrapper = FileWrapper( open( path ) )
		response=HttpResponse(wrapper, content_type="application/txt")
		response['Content-Disposition'] ='attachment; filename="results_2b_phaseA.json"'
		return response
        else:
		return render_to_response("Task1B-A.html", {"errors":"No File."}, RequestContext(request))






def task2b(request):
	return render_to_response("Task2b.html", RequestContext(request))



#Submit View and upload results functionanlity
@login_required
def task1ba(request):
	active=Detail1b.objects.filter(phase="A").filter(finished__gte=datetime.now()).filter(started__lte=datetime.now())
	if active:
		active=active[0]
	else:
		active=None	
	attempts=[item for item in user_results_1b.objects.all() if item.user == User.objects.get(username=request.user) and item.test_id in [x for x in Detail1b.objects.filter(phase="A").filter(test_id__gte=4)]]
	tests=Detail1b.objects.filter(phase="A").filter(test_id__gte=4).filter(started__lte=datetime.now())
	user=request.user
	errors=[]
	if request.method=='POST': #If the user submits data...
		form = DocumentForm(request.POST, request.FILES)
		form.fields['system_name'].queryset=system.objects.filter(user=request.user)
		if form.is_valid():
			c=form.cleaned_data
			systems=system.objects.get(system=c['system_name'])
			try: 
				user_data_raw=request.FILES['docfile'].read()
				user_data=json.loads(user_data_raw)
			except:
				errors.append("Error while decoding the JSON. Valid JSON?")
				a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
				return render_to_response("Task1B-A.html", {"tests":tests, "attempts":attempts, "current_test":active, "errors":errors, "form":form}, RequestContext(request))
			#Having the valid user JSON make whatever checks you want	
			test_ids=[]
			actives=golden_question_1b.objects.filter(testset=active)
			for question in actives:
				test_ids.append(question.question_id)
			#Check that the user submits data for every question
			if not len(user_data['questions'])==active.number_of_questions:
				errors.append("Error! The number of the questions in the JSON is different from the number of questions in the active test set.") 
				a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
				return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active,"attempts":attempts, "errors":errors, "form":form}, RequestContext(request))	
			for question in user_data['questions']:
				#Check that the PMIDs submitted belong to active PMIDs
				try: 
					if not question['id'] in test_ids:
						errors.append("Error! Question id: %s. The question id doesn't belong to the active test set." %question['id']) 
  						a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
						return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active,"attempts":attempts, "errors":errors, "form":form}, RequestContext(request))
				except:
					errors.append("Error! Question id not found in one of the questions. Please make sure you submit the correct JSON format.")
					a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
					return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))		
				flag=0
				#Each list of concepts, articles, snippets, triples has less than 100 elements
				try: 
					if len(question['documents'])>100:
						errors.append("Error! Question id: %s. The documents were more than 100." %question['id'])
						a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
						return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active,"attempts":attempts, "errors":errors, "form":form}, RequestContext(request))
				except: 	 
					flag+=1
				try: 
					if len(question['snippets'])>100:
						errors.append("Error! Question id: %s. The snippets were more than 100." %question['id'])
						a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
						return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
				except: 	 
					flag+=1
				try: 
					if len(question['concepts'])>100:
						errors.append("Error! Question id: %s. The concepts were more than 100." %question['id'])
						a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
						return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
				except: 	 
					flag+=1
				try: 
					if len(question['triples'])>1000:
						errors.append("Error! Question id: %s. The triples were more than 1000." %question['id'])
						a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
						return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
				except: 	 
					flag+=1		
				if flag==4:
					errors.append("Error! Question id: %s. No annotations for this question found.. Please try again." %question['id'])
					a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
					return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
			#Save the file
			pt="/home/bioasq/public_html/webexample/uploads/users/task2b/phaseA/testset%d/%s.json" %(active.test_id, systems.system)
			try:
				f=open(pt, 'w')
				myfile=File(f)
				print>>myfile, user_data_raw
				myfile.close()
			except:
				errors.append("Error while saving the file. Try again later.")
				a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
				return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
			#Delete previous uploads for the same user, system, testset and update the database with information for the saved file
			entry2=user_results_1b.objects.filter(system=systems).filter(test_id=active).delete()	
			entry2=user_results_1b(system=systems, user=user,  test_id=active, path=pt, datatime=datetime.now()).save()
			##TEMP: Show evaluation measures:
			errors.append("Results saved successfully!")
			a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment=errors[0]).save()
			return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
	form=DocumentForm()
	form.fields['system_name'].queryset=system.objects.filter(user=user)
	return render_to_response("Task1B-A.html", {"tests":tests, "current_test":active, "errors":errors,"attempts":attempts, "form":form}, RequestContext(request))
		

@csrf_exempt
def Task1bPhaseASubmitAPI(request, pk):
	if request.method=='POST':
		active=Detail1b.objects.filter(phase="A").filter(finished__gte=datetime.now())
		if not active:
			return HttpResponse("Currently, there is no test set active, in order to upload your results!\n")
		else:
			active=active[0]
		try:
			distro=int(pk)+3
		except:
			return HttpResponse("Error: The integer that corresponds to the active test set in the URI caused an error. Check the URI format.\n")
		if not active.test_id==distro:
			return HttpResponse("Error: The test set you provided in the URL doesn't match the currently active test set. Check and try again. \n")		
		try:
			data_raw=request.raw_post_data
			user_data=json.loads(data_raw)
		except:
			return HttpResponse("Error during decoding JSON. Valid JSON object?\n")
		try:
			user=authenticate(username=user_data['username'], password=user_data['password'])	
		except:
			return HttpResponse("Error: Make sure you have username and password fields in the JSON. Check the JSON format.\n")
		if user is None:
			return HttpResponse("There was a problem during your authentication. Please, check your username and your password! \n")
		if not user.is_active:
			return HttpResponse("Your account is not active. Please click on the activation link or contact the administrations.\n")	
		try:
			systems=system.objects.filter(user=user).get(system=user_data["system"])
		except: 
			return HttpResponse("Error: The system name you have put in your JSON string does not belong to you or it does not exist.\n")
		#Having the valid user JSON make whatever checks you want	
		test_ids=[]
		actives=golden_question_1b.objects.filter(testset=active)
		for question in actives:
			test_ids.append(question.question_id)
		#Check that the user submits data for every question
		if not len(user_data['questions'])==active.number_of_questions:
			return HttpResponse("Error! The number of the questions in the JSON is different from the number of questions in the active test set.\n" )	
		for question in user_data['questions']:
			#Check that the PMIDs submitted belong to active PMIDs
			try: 
				if not question['id'] in test_ids: 
					return HttpResponse("Error! Question id: %s. The question id doesn't belong to the active test set.\n" %question['id'])
			except:
				return HttpResponse("Error! Question id not found. Please make sure you submit the correct JSON format.\n")		
			
			#Each list of concepts, articles, snippets, triples has less than 100 elements
			flag=0
			try: 
				if len(question['documents'])>100:
					return HttpResponse("Error! Question id: %s. The documents were more than 100.\n" %question['id'])
			except: 	 
				flag+=1
			try: 
				if len(question['snippets'])>100:
					return HttpResponse("Error! Question id: %s. The snippets were more than 100.\n" %question['id'])
			except: 	 
				flag+=1
			try: 
				if len(question['concepts'])>100:
					return HttpResponse("Error! Question id: %s. The concepts were more than 100.\n" %question['id'])
			except: 	 
				flag+=1
			try: 
				if len(question['triples'])>100:
					return HttpResponse("Error! Question id: %s. The triples were more than 100.\n" %question['id'])
			except: 	 
				flag+=1		
			if flag==4:
				return HttpResponse("Error! Question id: %s. No annotations for this question found.. Please try again." %question['id'])
		#Save the file
		pt="/home/bioasq/public_html/webexample/uploads/users/task2b/phaseA/testset%d/%s.json" %(active.test_id, systems.system)
		try:
			f=open(pt, 'w')
			myfile=File(f)
			print>>myfile, data_raw
			myfile.close()
		except:
			a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment="Using the API: Error while saving the file. Try again later.").save()

			HttpResponse("Error while saving the file. Try again later.\n")
		#Delete previous uploads for the same user, system, testset and update the database with information for the saved file
		entry2=user_results_1b.objects.filter(system=systems).filter(test_id=active).delete()	
		entry2=user_results_1b(system=systems, user=user,  test_id=active, datatime=datetime.now(),  path=pt).save()
		a=upload_information_for_1b(user=user, system=systems, test_id=active, timestamp=datetime.now(), comment="Using the API: Results saved successfully!").save()
                
  		return HttpResponse("Results saved successfully!\n")
	else:	
		return HttpResponse("You need to use the 'POST' method in your Http Request.\n")





def evaluate_1b(request):
	com=[]
	for test in Detail1b.objects.filter(phase="A").filter(test_id__gte=4):
		if not test.is_oracle:
			for participant in user_results_1b.objects.filter(test_id=test):
				evaluation_measures_1b.objects.filter(user=participant.system).filter(testset=test).delete()
				e=evaluation_measures_1b(testset= test, user=participant.system,  mp_con=-1, mr_con=-1, f_con=-1,     MAP_con=-1, GMAP_con=-1, mp_art=-1, mr_art=-1, f_art=-1, MAP_art=-1, GMAP_art=-1, mp_snip=-1, mr_snip=-1, f_snip=-1, MAP_snip=-1, GMAP_snip=-1, mp_trip=-1, mr_trip=-1, f_trip=-1, MAP_trip=-1, GMAP_trip=-1).save()

		else:
			#gold_results=test.golden_path #I modify it when I got the golden data of the year
			gold_results='/home/bioasq/public_html/webexample/task1b/golden_files/golden2ndyear.json'			
			for participant in user_results_1b.objects.filter(test_id=test):
				system_results=participant.path
				command='java -cp $CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar evaluation.EvaluatorTask1b -phaseA  {0} {1} /home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/PMCdocslist.txt'.format(gold_results, system_results)
				#com.append(command)		
				result=subprocess.Popen(command.split(),  stdout=subprocess.PIPE)
				p=result.communicate()
				a=p[0].split() #this is string and I am spliting it...
				com.append(a)
				#writeCSV(participant.system.system, a)
				evaluation_measures_1b.objects.filter(user=participant.system).filter(testset=test).delete()
				e=evaluation_measures_1b(testset= test, user=participant.system,  mp_con=float(a[0]), mr_con=float(a[1]), f_con=float(a[2]),MAP_con=float(a[3]), GMAP_con=float(a[4]), mp_art=float(a[5]), mr_art=float(a[6]), f_art=float(a[7]), MAP_art=float(a[8]), GMAP_art=float(a[9]), mp_snip=float(a[10]), mr_snip=float(a[11]), f_snip=float(a[12]), MAP_snip=float(a[13]), GMAP_snip=float(a[14]), mp_trip=float(a[15]), mr_trip=float(a[16]), f_trip=float(a[17]), MAP_trip=float(a[18]), GMAP_trip=float(a[19])).save()
				#e=evaluation_measures_1b(testset= test, user=participant.system,  mp_con=float(a[0]), mr_con=float(a[1]), f_con=float(a[2]),MAP_con=float(a[3]), GMAP_con=float(a[4]), mp_art=float(a[5]), mr_art=float(a[6]), f_art=float(a[7]), MAP_art=float(a[8]), GMAP_art=float(a[9]), mp_snip=-1, mr_snip=-1, f_snip=-1, MAP_snip=-1, GMAP_snip=-1, mp_trip=float(a[15]), mr_trip=float(a[16]), f_trip=float(a[17]), MAP_trip=float(a[18]), GMAP_trip=float(a[19])).save()
	return HttpResponse("Done, I just calculated the measures for Phase A of task 2b")



def writeCSV(s, scores):
	for score in scores:
		scores=[format(float(x), ".6f") for x in scores]
	with open('/home/bioasq/public_html/webexample/task1b/junk/TEMP_Results.csv', 'a') as out:
		writer=csv.writer(out, delimiter='\t')
		writer.writerow([s]+scores)
