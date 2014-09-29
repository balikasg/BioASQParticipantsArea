# Create your views here.
# Create your views here.
from forms import OracleForm, OracleSelectVisibleForm, getDataForm
from Test.models import *
from task1b.models import *
from task1bb.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import json, subprocess, requests, os, time, sys
from django.core.files import File
from os import listdir
from datetime import datetime
from models import *
from django.core.mail import EmailMessage
from django.contrib import messages
import os


def filterer(request):
	if request.GET['q'] == '1': 
		return HttpResponse(json.dumps(get_my_choices()))
	elif request.GET['q'] == '1ba': 
		return HttpResponse(json.dumps(get_my_choicesB()))
	elif request.GET['q'] == '1bb': 
		return HttpResponse(json.dumps(get_my_choicesBB()))
	else:
		return HttpResponse(json.dumps(0))
		
def get_my_choices():
	lista=[]
	for a in Detail.objects.filter(is_oracle=True).filter(test_id__gte=2).filter(test_id__lte=19):
		if a.test_id <= 7:
			lista.append({"pk":str(a.test_id),"name":"Task 1a: Test batch 1, Week %s" %(a.test_id-1)})
		elif a.test_id <= 13:
			lista.append({"pk":str(a.test_id),"name":"Task 1a: Test batch 1, Week %s" %(a.test_id-7)})	
		elif a.test_id <= 19:
			lista.append({"pk":str(a.test_id),"name":"Task 1a: Test batch 1, Week %s" %(a.test_id-13)})
		else:
			lista.append((str(a.test_id),"Task 1a: Additional test batch 4, Week %s" %(a.test_id-1-18)))
	return (lista)



def get_my_choicesB():
        lista=[]
	for a in Detail1b.objects.filter(phase='A').filter(is_oracle=True).filter(test_id__lte=3):
		if a.test_id <= 7:
			lista.append({'pk':int(a.test_id), 'name':'Task 1B-Phase A, Batch %d' %a.test_id})
		else:
			lista.append({'pk':int(a.test_id), 'name':'Task 2B-Phase A, Batch %d' %(a.test_id-3)})
	return lista

def get_my_choicesBB():
        lista=[]
        for a in Detail1b.objects.filter(phase='B').filter(is_oracle=True).filter(test_id__lte=3):
		if a.test_id <= 7:
                        lista.append({'pk':int(a.test_id), 'name':'Task 1B-Phase B, Batch %d' %a.test_id})
                else:
                        lista.append({'pk':int(a.test_id), 'name':'Task 2B-Phase B, Batch %d' %(a.test_id-3)})
        return lista







@login_required
def taskAData(request):
	form=getDataForm()
	if request.method=='POST':
		form3 = getDataForm(request.POST)
                if form3.is_valid():
               		c=form3.cleaned_data
	                test=(int(c["testset"]))
			if not c['vectorized']:
				return HttpResponseRedirect("/data/raw/%d/" %test)
			else: 
				return HttpResponseRedirect("/data/vectorized/%d/" %test)
		#make sure to update the counter.
	return  render_to_response("getData.html", {"form":form},  RequestContext(request))


def makeGoldenDatabase(request):
	lines=open('/home/bioasq/public_html/webexample/name_id_mapping2013.txt', 'r').read().splitlines()
        c=dict(line.split('=') for line in lines)
        tests=Detail.objects.filter(test_id__gte=2).filter(test_id__lte=19)
	cnt=0
	for test in tests:
	        articles=Article.objects.filter(distro=test)
		with open('/home/bioasq/public_html/webexample/test%dpmids' %test.test_id, 'r') as input: #HERE
                	pmid_list=json.load(input)	
	        data={"getMajorMeshFor":[pmid_list]}
        	data={"json":json.dumps(data).encode('utf-8')}
	        s=requests.Session()
        	tmplink=s.get("http://www.gopubmed.org/web/gopubmedbeta/bioasq/pubmed")
	        res=s.post(tmplink.text, data=data)
        	d=json.loads(res.text)
		mes=["Testing"]
        	try:
                	if d['result']==[]:
                        	return mes.append("The web service didn't return anything for the test set %d!" %test.test_id)
	                mes.append("Testset: %d\nAnnotated Articles: %d/%d" %((test.test_id-1), len(d['result']), test.number_of_abstracts  ))
        	except:
                	return HttpResponse("An error with the web service that returns the annotations occured. Please try again later. The error was in testset %d." %test.test_id)
	        f=open("/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/true_labels.txt" %test.test_id, 'w')
        	myfile=File(f)
                	#Check for which PMIDs you received MeSH
	        pmid_list=[]
        	for i in range(len(d['result'])):
                	pmid_list.append(d['result'][i]['pmid'])
	                string=""
        	        #For each one of the PMIDs collect the MeSH
                	for j in range(len(d['result'][i]["majorMesh"])):
				try:
                        		string+=c[str(d['result'][i]["majorMesh"][j])] #Normally, this should be in indexes, but the web service returns HUMAN WORDS so I save from the dictionary I have initialized before
	                        	string+=" "
				except:
					cnt+=1			
        	        print>>myfile, string #Save the string in a file, where each line is an article (pmid-list)
	        myfile.close()
                #Make the Golden File you have just created in the format that is used during evaluation.
        	subprocess.call(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "converters.MapMeshResults", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mapping.txt", "/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/true_labels.txt" %test.test_id, "/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/golden_labels.txt" %test.test_id])
	        with open("/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/pmids.txt" %test.test_id, 'w') as out:
        	        json.dump(pmid_list, out)
	return HttpResponse(mes+ "There were %d articles lost." %cnt)


def saveVisible(sys, user, test, arr, w, isVisible):
	try:    
		old=eval_meas_oracle.objects.filter(user=sys).get(test_id=test)
                old.delete()
                eval_meas_oracle(user=sys, test_id=test, accuracy=float(arr[0]), ebp=float(arr[1]), example_based_recall=float(arr[2]), example_based_f=float(arr[3]), macro_precision=float(arr[4]), macro_recall=float(arr[5]), macro_f_measure=float(arr[6]), micro_precision=float(arr[7]), micro_recall=float(arr[8]), micro_f=float(arr[9]), hierarchical_precision=float(w[0]), hierarchical_recall=float(w[1]), hierarchical_f=float(w[2]), lca_p=float(w[3]), lca_r=float(w[4]),lca_f=float(w[5]),timestamp=datetime.now(), is_visible=isVisible).save()              
	except:
                eval_meas_oracle(user=sys, test_id=test, accuracy=float(arr[0]), ebp=float(arr[1]), example_based_recall=float(arr[2]), example_based_f=float(arr[3]), macro_precision=float(arr[4]), macro_recall=float(arr[5]), macro_f_measure=float(arr[6]), micro_precision=float(arr[7]), micro_recall=float(arr[8]), micro_f=float(arr[9]), hierarchical_precision=float(w[0]), hierarchical_recall=float(w[1]), hierarchical_f=float(w[2]), lca_p=float(w[3]), lca_r=float(w[4]),lca_f=float(w[5]),timestamp=datetime.now(), is_visible=isVisible).save()



def saveVisiblePhaseA(sys, user, test, a, isVisible):
	try:
                old=eval_meas_oracle_1b.objects.filter(user=sys).get(test_id=test)
                old.delete()
	except:
		pass
	eval_meas_oracle_1b(user=sys, test_id=test, mp_con=float(a[0]), mr_con=float(a[1]), f_con=float(a[2]),     MAP_con=float(a[3]), GMAP_con=float(a[4]), mp_art=float(a[5]), mr_art=float(a[6]), f_art=float(a[7]), MAP_art=float(a[8]), GMAP_art=float(a[9]), mp_snip=float(a[10]), mr_snip=float(a[11]), f_snip=float(a[12]), MAP_snip=float(a[13]), GMAP_snip=float(a[14]), mp_trip=float(a[15]), mr_trip=float(a[16]), f_trip=float(a[17]), MAP_trip=float(a[18]), GMAP_trip=float(a[19]), timestamp=datetime.now(), is_visible=isVisible).save()



def saveVisiblePhaseB(sys, user, test, a, isVisible):
        try:
                old=eval_measi_oracle_1bb.objects.filter(system=sys).get(testset=test)
                old.delete()
        except:
                pass
	try:
                e=eval_measi_oracle_1bb(testset=test, system=sys, acc=float(a[0]), s_acc=float(a[1]), l_acc=float(a[2]), mrr=float(a[3]), prec=float(a[4]), rec=float(a[5]), fmeas=float(a[6]), r2p=float(a[7]), r2r=float(a[8]), r2f=float(a[9]), r4p=float(a[10]), r4r=float(a[11]), r4f=float(a[12]), read=-1, recall=-1, rep=-1, preci=-1, timestamp=datetime.now(), is_visible=isVisible).save()
        except:
                e=eval_measi_oracle_1bb(testset=test, system=sys, acc=0, s_acc=0, l_acc=0, mrr=0, prec=0, rec=0, fmeas=0, r2p=float(a[0]), r2r=float(a[1]), r2f=float(a[2]), r4p=float(a[3]), r4r=float(a[4]), r4f=float(a[5]), read=-1, recall=-1, rep=-1, preci=-1, timestamp=datetime.now(), is_visible=isVisible).save()



@login_required
def oracle(request):
	user=request.user
	form=OracleForm()
        form.fields['system_name'].queryset=system.objects.filter(user=user)
	if request.method=='POST':
		if 'saveResults' in request.POST:
			form3 = OracleSelectVisibleForm(request.POST)
			if form3.is_valid():
				c=form3.cleaned_data
				data=json.loads(c['hid'])
				sys=system.objects.get(system=data['sys'])
				if data['task'] == 'A':
					arr, w=data['arr'], data['w']
					test=Detail.objects.get(test_id=(int(data["test"])))
			 		if c['keep_score']:
						if c['is_visible']:
							saveVisible(sys, user, test, arr, w, True)
							message=['Your results were saved and are visible.']
						else:
							saveVisible(sys, user, test, arr, w, False)
							message=["Your results were saved, but are visible only to you."]
					else:
						message=["Your results were not saved."]
					otherResults=[item for item in eval_meas.objects.filter(test_id=test)]
					oracleResults=[item for item in eval_meas_oracle.objects.filter(test_id=test) if (item.is_visible == True or item.user.user == user)] 
					return  render_to_response("oracle.html", { "message":message, "form":form, "oracleResults":oracleResults, 'other':otherResults}, RequestContext(request))			
				elif data['task'] == 'phaseA':
					a=data['arr']
					test=Detail1b.objects.filter(phase='A').get(test_id=(int(data["test"])))	
					if c['keep_score']:
						if c['is_visible']:
							saveVisiblePhaseA(sys, user, test, a, True)
							message=['Your results were saved and are visible.']
						else:
							saveVisiblePhaseA(sys, user, test, a, False)
							message=["Your results were saved, but are visible only to you."]
					else: 
						message=["Your results were not saved."]
					otherResults=[item for item in evaluation_measures_1b.objects.filter(testset=test)]
					oracleResultsPhaseA=[item for item in eval_meas_oracle_1b.objects.filter(test_id=test) if (item.is_visible == True or item.user.user == user)]
					message.append(len(otherResults))
					return  render_to_response("oracle.html", {'message':message, "taskB":otherResults, "taskBoracle":oracleResultsPhaseA, "form":form}, RequestContext(request))
				elif data['task'] == 'phaseB':
					a=data['arr']
					test=Detail1b.objects.filter(phase='B').get(test_id=(int(data["test"])))
					if c['keep_score']:
                                                if c['is_visible']:
                                                        saveVisiblePhaseB(sys, user, test, a, True)
                                                        message=['Your results were saved and are visible.']
                                                else:
                                                        saveVisiblePhaseB(sys, user, test, a, False)
                                                        message=["Your results were saved, but are visible only to you."]
                                        else:
                                                message=["Your results were not saved."]
                                        otherResults=[item for item in evaluation_measures_1bb.objects.filter(testset=test)]
                                        oracleResultsPhaseB=[item for item in eval_measi_oracle_1bb.objects.filter(testset=test) if (item.is_visible == True or item.system.user == user)]
                                        return  render_to_response("oracle.html", {'message':message, "taskBB":otherResults, "taskBBoracle":oracleResultsPhaseB, "form":form}, RequestContext(request))
				else: 
					return HttpResponse("Disaster")
		if 'submitResults'in request.POST:
			ok=0
			mes=[]
			form = OracleForm(request.POST, request.FILES)
			form.fields['system_name'].queryset=system.objects.filter(user=request.user)
			if not form.is_valid():
				return  render_to_response("oracle.html", { "message":["Error while filling the form!"], "form":form}, RequestContext(request))
			else:
				c=form.cleaned_data
				systems=system.objects.get(system=c['system_name'])
				try: 
					user_data=json.loads(request.FILES['docfile'].read())
				except:
					mes.append("\n Error while decoding the JSON string.")
					return render_to_response("oracle.html", { "message":mes, "form":form}, RequestContext(request))
				sys=system.objects.get(system=c['system_name'])
				if c['task']=="1":
					test=Detail.objects.get(test_id=(int(c["test"])))
					otherResults=[item for item in eval_meas.objects.filter(test_id=test)]
					(mes, arr, w)=eval1a(user_data, test)	
					try:
						otherResults.append(eval_meas(user=system.objects.get(system='ORACLE'), test_id=test, accuracy=float(arr[0]), ebp=float(arr[1]), example_based_recall=float(arr[2]), example_based_f=float(arr[3]), macro_precision=float(arr[4]), macro_recall=float(arr[5]), macro_f_measure=float(arr[6]), micro_precision=float(arr[7]), micro_recall=float(arr[8]), micro_f=float(arr[9]), hierarchical_precision=float(w[0]), hierarchical_recall=float(w[1]), hierarchical_f=float(w[2]), lca_p=float(w[3]), lca_r=float(w[4]),lca_f=float(w[5])))
					
						log_oracle(user=user, system=sys, test_id=test, timestamp=datetime.now(), comment=("Using the oracle: "+" ".join(mes)+"Flat measures: "+", ".join(arr) +" Hierarchical Measures: "+", ".join(w))).save()
						ok=1
					except:
						return render_to_response("oracle.html", { "message":mes,  "system":systems,  "form":form} , RequestContext(request))
					oracleResults=[item for item in eval_meas_oracle.objects.filter(test_id=test) if (item.is_visible == True or item.user.user == user)]
					sendMail(sys.system_description, test.test_id-1, user.email, arr, w)
					form2=OracleSelectVisibleForm(initial={'hid':json.dumps({'arr':arr, 'w':w, 'task':"A",  'test':test.test_id, 'sys':sys.system})})
					return render_to_response("oracle.html", { "ok": ok, "message":mes, "oracleSelect":form2, "oracleResults":oracleResults, "system":systems, "flat":arr, "hier":w, "form":form, 'other':otherResults}, RequestContext(request))
				elif c['task']=='1ba':
					test=Detail1b.objects.filter(phase="A").get(test_id=(int(c["test"])))
					mes, a=eval1b(user_data, test.test_id)
					otherResults=[item for item in evaluation_measures_1b.objects.filter(testset=test)]
					otherResults.append(evaluation_measures_1b(user=system.objects.get(system='ORACLE'), testset=test, mp_con=float(a[0]), mr_con=float(a[1]), f_con=float(a[2]),     MAP_con=float(a[3]), GMAP_con=float(a[4]), mp_art=float(a[5]), mr_art=float(a[6]), f_art=float(a[7]), MAP_art=float(a[8]), GMAP_art=float(a[9]), mp_snip=float(a[10]), mr_snip=float(a[11]), f_snip=float(a[12]), MAP_snip=float(a[13]), GMAP_snip=float(a[14]), mp_trip=float(a[15]), mr_trip=float(a[16]), f_trip=float(a[17]), MAP_trip=float(a[18]), GMAP_trip=float(a[19])))
					form2=OracleSelectVisibleForm(initial={'hid':json.dumps({'arr':a, 'task':"phaseA", 'test':test.test_id, 'sys':sys.system})})
					return render_to_response("oracle.html", {"taskB":otherResults, "form":form, "oracleSelect":form2, 'ok':1}, RequestContext(request))
				else:
					test=Detail1b.objects.filter(phase="B").get(test_id=(int(c["test"])))
					a, b=eval1bb(user_data, test)
					otherResults=[i for i in evaluation_measures_1bb.objects.filter(testset=test) if i.acc > 0.001 or i.s_acc > 0.001 or i.prec > 0.001]
					try: 
						otherResults.append(evaluation_measures_1bb(testset=test, system=system.objects.get(system='ORACLE'), acc=a[0], s_acc=a[1], l_acc=a[2], mrr=a[3], prec=a[4], rec=a[5], fmeas=a[6], r2p=b[0], r2r=b[1], r2f=b[2], r4p=b[3], r4r=b[4], r4f=b[5]))
					except:
						a=[0,0,0,0,0,0,0]
						otherResults.append(evaluation_measures_1bb(testset=test, system=system.objects.get(system='ORACLE'), acc=a[0], s_acc=a[1], l_acc=a[2], mrr=a[3], prec=a[4], rec=a[5], fmeas=a[6], r2p=b[0], r2r=b[1], r2f=b[2], r4p=b[3], r4r=b[4], r4f=b[5]))
					form2=OracleSelectVisibleForm(initial={'hid':json.dumps({'arr':a+b, 'task':"phaseB", 'test':test.test_id, 'sys':sys.system})})
                                        return render_to_response("oracle.html", {"taskBB":otherResults, "form":form, "oracleSelect":form2, 'ok':1}, RequestContext(request))
	return render_to_response("oracle.html", {"form":form}, RequestContext(request))	





def resultsOracleTaskA(request):
	user=request.user
        tests=Detail1b.objects.filter(phase="A").filter(test_id__gte=1).filter(test_id__lte=3)
        evaluation=evaluation_measures_1b.objects.all()
	otherResults=[item for item in eval_meas_oracle_1b.objects.all() if (item.is_visible == True or item.user.user == user)]	
        return render_to_response('resultsOracleTaskA.html', {"tests":tests, "otherResults": otherResults, "evaluation":evaluation }, RequestContext(request))

def resultsOracleTaskB(request):
        user=request.user
        tests=Detail1b.objects.filter(phase="B").filter(test_id__gte=1).filter(test_id__lte=3)
        evaluation=evaluation_measures_1bb.objects.all()
        otherResults=[item for item in eval_measi_oracle_1bb.objects.all() if (item.is_visible == True or item.system.user == user)]
        return render_to_response('resultsOracleTaskB.html', {"tests":tests, "otherResults": otherResults, "evaluation":evaluation }, RequestContext(request))


def eval1b(g, test):
	tests=Detail1b.objects.filter(phase="A").get(test_id=test)
	mes=[]
	try:
		if not tests.number_of_questions == len(g['questions']):
			mes.append("Different number of questions between the official test set and the JSON you submitted.\nThe official test set %d consists of %d questions.\nThere are %d questions in the JSON string you submitted." %(test, tests.number_of_questions, len(g['questions'])))
	                return (mes, [])
	except:
		mes.append('Error with the fields in the JSON you submitted.\nThe JSON should begin with "questions"\nCheck the online guidelines for details about the format of the JSON string.')
                return (mes, [])
	path="/home/bioasq/public_html/webexample/oracle/temp/temp.json"
	with open(path, 'w') as out:
		json.dump(g, out)
	command='java -cp $CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluationWithIoannis.jar evaluation.EvaluatorTask1b -phaseA {0} {1} /home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/PMCdocslist.txt'.format(tests.golden_path, path)
	#command='java -cp $CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluationSeptember5_2014.jar evaluation.EvaluatorTask1b -phaseA  {0} {1}'.format(tests.golden_path, path)
	result=subprocess.Popen(command.split(),  stdout=subprocess.PIPE)
	p=result.communicate()
	#mes.append("Test set: %d\nQuestions: %d" %(tests.test_id, tests.number_of_questions))
	os.remove(path)
	return ("I was in the eval function", p[0].split())



def eval1bb(g, test):
	path="/home/bioasq/public_html/webexample/oracle/temp/temp-phaseB.json"
	with open(path, 'w') as out:
		os.chmod(path, 0o777)
		json.dump(g, out)
	#com='java -cp $CLASSPATH:/home/bioasq/public_html/webexample/task1b/measures/BioASQEvaluation.jar evaluation.EvaluatorTask1b -phaseB  {0} {1}'.format(test.golden_path, path)
	com='java -cp $CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar evaluation.EvaluatorTask1b -phaseB  {0} {1} /home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/PMCdocslist.txt'.format(test.golden_path, path)
	result=subprocess.Popen(com.split(),  stdout=subprocess.PIPE)
	p=result.communicate()
	a=p[0].split()
	#return a 
	com='python /home/bioasq/public_html/webexample/task1bb/rouge-bioasq/rouge.py {0} {1}'.format(test.golden_path, path)
	#com="python /home/bioasq/public_html/webexample/task1bb/rouge-bioasq/rouge.py /home/bioasq/public_html/webexample/task1b/golden_files/golden_05.json /home/bioasq/public_html/webexample/oracle/temp/temp-phaseB.json"
	proc = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	os.remove(path)
	return a, out[1:-2].split(', ')


	
def eval1a(g, test):
	mes=[]
	if test.is_oracle== False:
		mes.append("The test set %d is not available for use in the oracle yet." %(test.test_id-1))
		return (mes, [], [])
	try:
		len(g["documents"])
		g['documents'][0]['pmid']
		len(g['documents'][0]['labels'])
	except:
		mes.append("Error decoding the fields of the JSON you submitted.\nAlthough it is a valid JSON object, it seems there is a problem with the names of the fields.\n Notice that the names of the fields for the JSON of Task 1A are: 'documents', 'labels' and 'pmid'.")
                return (mes, [], [])
	if not len(g['documents']) == int(test.number_of_abstracts_oracle):
		mes.append("Different number of documents between the official test set and the JSON you submitted.\nThe official test set you selected contains %d articles. Your JSON contains %d." %(test.number_of_abstracts_oracle, len(g['documents'])))
		return (mes, [], [])
	lines=open('/home/bioasq/public_html/webexample/name_id_mapping2013.txt', 'r').read().splitlines()
	c=dict(line.split('=') for line in lines)
	pmid_list=json.loads(open('/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/pmids.txt' %(test.test_id)).read())
	#After having the golden, try for each system..	
	f=open("/home/bioasq/public_html/webexample/oracle/temp/system_A_results.txt", 'w')
	myfile=File(f)
	string=""
	mes.append("Annotated documents: %d out of %d." %(len(pmid_list), test.number_of_abstracts_oracle))
	for i in range(len(pmid_list)):
	        q=[element for element in g['documents'] if int(element['pmid'])==int(pmid_list[i])][0]
		string=""
		for k in range(len(q['labels'])):
			if q['labels'][k] in c.values():
                        	string+=q['labels'][k]
                                string+=" "
		if string=="":
			string+="D005260"
                print>>myfile, string
	myfile.close()
	subprocess.call(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "converters.MapMeshResults", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mapping2013.txt", "/home/bioasq/public_html/webexample/oracle/temp/system_A_results.txt", "/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt"])
				#I need to run for the flat measures
	result=subprocess.Popen(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "evaluation.Evaluator", "/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/golden_labels.txt" %test.test_id, "/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt"], stdout=subprocess.PIPE)
	p=result.communicate()
	arr=p[0].split() #this is string and I am spliting it...	
	result=subprocess.Popen(["/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/hierarchical/bin/HEMKit", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mesh_hier_int2013.txt", "/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/golden_labels.txt" %test.test_id, "/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt", "4", "5"], stdout=subprocess.PIPE)
	s=result.communicate()
	w=s[0].split()
	os.remove("/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt")
	os.remove("/home/bioasq/public_html/webexample/oracle/temp/system_A_results.txt")		
	return (mes, arr, w)




def resultsOracle(request):
	user=request.user
	otherResults=[item for item in eval_meas_oracle.objects.all() if (item.is_visible == True or item.user.user == user)]
	evaluation=[item for item in eval_meas.objects.all()]
	tests=Detail.objects.filter(test_id__lte=19).filter(test_id__gte=2)
        return render_to_response('resultsOracle.html', {"evaluation":evaluation, "otherResults": otherResults, "tests":tests }, RequestContext(request))


def sendMail(system, test_id, email,arr, w):
	text="Your results"
	text+="\nSystem: %s\nTestset: %s\n" %(system, str(test_id))
	text+="Accuracy=%s,\n EbP=%s,\n EbR=%s,\n EbF=%s,\n MaP=%s,\n MaR=%s,\n MaF=%s,\nMiP=%s,\n MiR=%s,\n MiF=%s,\n HiP=%s,\n HiR=%s,\n HiF=%s,\n LCA-P=%s,\n LCA-R=%s,\n LCA-F=%s\n" %(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], w[0], w[1], w[2], w[3], w[4], w[5])
	EmailMessage("[BioASQ]: Oracle, Task 1A results", text, 'admin@bioasq.org', [email]).send()
