from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.http import HttpResponse
from Test.models import *
from django.core import serializers
from django.template import RequestContext
import datetime
from forms import *
import json, urllib, os
from django.core.servers.basehttp import FileWrapper
import xml.etree.ElementTree as ET
from django.core.files import File
import requests
from decorator import decorator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from datetime import datetime
from uploads.forms import DocumentForm
from uploads.models import Document
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from webservice.serializers import *
import subprocess, os
import urllib2, urllib, zipfile, StringIO, shutil
from django.conf import settings
from os import listdir
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from task1bb.rrouge import rouge
API_SSL_SERVER="https://www.google.com/recaptcha/api"
API_SERVER="http://www.google.com/recaptcha/api"
VERIFY_SERVER="www.google.com"

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (public_key,
                 use_ssl = False,
                 error = None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return """<script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>

<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>
""" % {
        'ApiServer' : server,
        'PublicKey' : public_key,
        'ErrorParam' : error_param,
        }


def submit (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len (recaptcha_response_field) and len (recaptcha_challenge_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode ({
            'privatekey': encode_if_necessary(private_key),
            'remoteip' :  encode_if_necessary(remoteip),
            'challenge':  encode_if_necessary(recaptcha_challenge_field),
            'response' :  encode_if_necessary(recaptcha_response_field),
            })

    request = urllib2.Request (
        url = "http://%s/recaptcha/api/verify" % VERIFY_SERVER,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read ().splitlines ();
    httpresp.close();

    return_code = return_values [0]

    if (return_code == "true"):
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values [1])

def check_captcha(request):
    remote_ip = request.META['REMOTE_ADDR']
    challenge = request.POST['recaptcha_challenge_field']
    response = request.POST['recaptcha_response_field']
    private_key="6LfOBd4SAAAAADPvwlFmcUvKdUZgAsbNRaLY-ce7"
    return submit(challenge, response, private_key, remote_ip)





# for downloading files with the test set
@login_required
def download_test(request, distro):
	try:
		distro=int(distro)
		target=Detail.objects.filter(started__lte=datetime.now()).get(test_id=distro)
	except ValueError:
		raise Http404
	except:
		dictionary=getDict(request.user)
                dictionary['error']=["The test you requested is not currently active.\n"]
		return render_to_response('Task2a.html',dictionary, RequestContext(request))
	path=target.path_raw
	target.number_of_downloads+=1
	downs=json.loads(target.downloaders)
        downs.append(str(request.user.username))
        target.downloaders=json.dumps(downs)
	target.save()
	wrapper = FileWrapper( open( path, "r" ) )
	name=get_my_data(distro)+"raw.json"
	response=HttpResponse(wrapper, content_type="text/plain")
	response['Content-Disposition'] ='attachment; filename="%s"' %name
	return response


def getDict(user):
	try:
	        active=Detail.objects.filter(finished__gte=datetime.now()).filter(started__lte=datetime.now())[0]
        except:
                active=None
        tests=Detail.objects.filter(test_id__gte=41).filter(started__lte=datetime.now())
        attempts=test_result_file.objects.filter(test_id__gte=41).filter(user=user)
        return {"tests":tests, "current_test":active, "attempts":attempts,} 





def get_my_data(distro):
        if distro == 1:
		return "Task1aDryRun_"
        elif distro <= 7:
		return "Task1a-Batch1-Week%d_" %(distro-1)
        elif a.test_id <= 13:
		return "Task1a-Batch2-Week%d_" %(distro-7)
        elif a.test_id <= 19:
		return "Task1a-Batch3-Week%d_" %(distro-13)
        elif a.test_id <= 40:
		return "Task1a-AdditionalBatch-Week%d_" %(distro-19)
        elif a.test_id == 41:
		return "Task2aDryRun_"
        elif a.test_id <= 46:
		return "Task2a-Batch1-Week%d_" %(distro-41)
        elif a.test_id <= 51:
		return "Task2a-Batch2-Week%d_" %(distro-46)
        elif a.test_id <= 56:
		return "Task2a-Batch3-Week%d_" %(distro-51)
	else:
		return "Task2a-AdditionalBatch-Week%d_" %(distro-56)
	


def download_vect_test(request, distro):
        try:
                distro=int(distro)
		target=Detail.objects.filter(started__lte=datetime.now()).get(test_id=distro)
        except ValueError:
                raise Http404
		
        errors=[]
        target=Detail.objects.get(test_id=distro)
        path=target.path_vect
	target.number_of_downloads+=1
	downs=json.loads(target.downloaders)
        downs.append(str(request.user.username))
        target.downloaders=json.dumps(downs)
        target.save()
        wrapper = FileWrapper( open( path ) )
	name=get_my_data(distro)+"lucene.zip"
        response=HttpResponse(wrapper, content_type="application/zip")
        response['Content-Disposition'] ='attachment; filename="%s"' %name
        return response

@login_required
def download_results(request, ts, s):
	try: 
		sys=system.objects.filter(user=request.user).get(system=s)
	except:
		raise Http404
	mes=""
	if not sys:
		mes+="Error. Bad url, regarging the system name."
		raise Http404
	test=Detail.objects.get(test_id=ts)
	if not test:

		mes+="Error. The test id you selected to download results doesn't exist."
		raise Http404
	p=test_result_file.objects.filter(test_id=test).filter(system=sys)
	if p:
		path=p[0].path
		wrapper = FileWrapper(open(path))
		response=HttpResponse(wrapper, content_type="application/txt")
		name="%s-%s.json" %(get_my_data(p[0].test_id.test_id),p[0].system)
		response['Content-Disposition'] ='attachment; filename=%s' %name
		return response	
	else:
		mes+="Error. No results uploaded for this system in the active test set."
		raise Http404 


def journals(request):
        path="/home/bioasq/public_html/webexample/TestJournalList.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="JournalList.txt"'
        return response

def journalsTraining(request):
        path="/home/bioasq/public_html/webexample/listOfJournalsTraining.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="JournalListOfTraining.txt"'
        return response


@login_required
def download_mesh2013(request):
        the_file = '/home/bioasq/public_html/webexample/TrainingData2014/MeSH2013.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


def word2vec(request):
	the_file = '/home/bioasq/public_html/webexample/word2vecTools.tar.gz'
        target=Detail.objects.get(test_id=-1)
        target.number_of_downloads+=1
        downs=json.loads(target.downloaders)
        target.save()	
	filename = os.path.basename(the_file)
	response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
	response['Content-Length'] = os.path.getsize(the_file)    
	response['Content-Disposition'] = "attachment; filename=%s" % 'biomedicalWordVectors.tar.gz'
	return response		


def word2vecRead(request):
        the_file = '/home/bioasq/public_html/webexample/README_BioASQ_word_vectors.pdf'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % 'BioASQ_word_vectors.pdf'
        return response



@login_required
def download_vect(request):
        the_file = '/home/bioasq/public_html/webexample/PubMedWithMeSHVectorized.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response



@login_required
def download_vect2014(request):
        the_file = '/home/bioasq/public_html/webexample/TrainingData2014/lucene-allMeSH.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

@login_required
def download_raw2014Limit(request):
        the_file = '/home/bioasq/public_html/webexample/TrainingData2014/allMeSH_limitjournals.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

@login_required
def download_vect2014Limit(request):
        the_file = '/home/bioasq/public_html/webexample/TrainingData2014/lucene-allMeSH_limitjournals.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

@login_required
def download_raw2014(request):
        the_file = '/home/bioasq/public_html/webexample/TrainingData2014/allMeSH.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

@login_required
def download_raw(request):
        the_file = '/home/bioasq/public_html/webexample/PubMedWithMeSH.zip'
        filename = os.path.basename(the_file)
        response = HttpResponse(FileWrapper(open(the_file)), content_type="application/force-download")
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


def sampleData1a(request):
        path="/home/bioasq/public_html/webexample/sampleData1a.json"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="BioASQ-SampleData1A.json"'
        return response

def sampleData1b(request):
        path="/home/bioasq/public_html/webexample/training1B.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="BioASQ-SampleData1B.json"'
        return response



@login_required
def d34(request):
        path="/home/bioasq/public_html/webexample/D3.4.Tutorials.Guidelines.pdf"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="application/pdf")
        response['Content-Disposition'] ='attachment; filename="BioASQ-D3_4.pdf"'
        return response

@login_required
def d41(request):
        path="/home/bioasq/public_html/webexample/wp4-specifications.pdf"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="application/pdf")
        response['Content-Disposition'] ='attachment; filename="BioASQ-EvalMeasures-taskB.pdf"'
        return response



def meshMapping(request):
        path="/home/bioasq/public_html/webexample/name_id_mapping.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="MeSH_name_id_mapping.txt"'
        return response

def meshMapping2014(request):
        path="/home/bioasq/public_html/webexample/TrainingData2014/name_id_mapping_2014.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="MeSH_name_id_mapping_2014.txt"'
        return response


@login_required
def training2b(request):
        path="/home/bioasq/public_html/webexample/TrainingData2014/BioASQ_2013_TaskB.zip"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="application/zip")
        response['Content-Disposition'] ='attachment; filename="BioASQ-trainingDataset2b.zip"'
        return response


def meshMapping2(request):
        path="/home/bioasq/public_html/webexample/MeSHparent_child_mapping.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="MeSH_parent_child_mapping.txt"'
        return response



def meshMappingPC2014(request):
        path="/home/bioasq/public_html/webexample/TrainingData2014/mesh_hier2014.txt"
        wrapper = FileWrapper( open( path, "r" ) )
        response=HttpResponse(wrapper, content_type="text/plain")
        response['Content-Disposition'] ='attachment; filename="MeSH_parent_child_mapping_2014.txt"'
        return response

@login_required
def tools(request):
        path="/home/bioasq/public_html/webexample/ExampleofVectorization.zip"
        wrapper = FileWrapper( open( path) )
        response=HttpResponse(wrapper, content_type="application/zip")
        response['Content-Disposition'] ='attachment; filename="VectorizationTools.zip"'
        return response


def api_documentation(request):
        path="/home/bioasq/public_html/webexample/task1b_api_documentation.zip"
        wrapper = FileWrapper( open( path) )
        response=HttpResponse(wrapper, content_type="application/zip")
        response['Content-Disposition'] ='attachment; filename="BioASQ_task1b_api_documentation.zip"'
        return response

@login_required
def cluster(request):
        path="/home/bioasq/public_html/webexample/BioASQ-Cluster.rar"
        wrapper = FileWrapper( open( path) )
        response=HttpResponse(wrapper, content_type="application/rar")
        response['Content-Disposition'] ='attachment; filename="BioASQ-Cluster.rar"'
        return response


#Task 2A
@login_required
def task2a(request):
	mes=""
	try:
		active=Detail.objects.filter(finished__gte=datetime.now()).filter(started__lte=datetime.now())[0]
	except:
		active=None
	tests=Detail.objects.filter(test_id__gte=41).filter(started__lte=datetime.now())
	errors=[] #This must be deleted probably
	form = DocumentForm(request.POST, request.FILES)
	form.fields['system_name'].queryset=system.objects.filter(user=request.user)
	attempts=test_result_file.objects.filter(test_id__gte=41).filter(user=request.user)
	if request.method=='POST': #If the user submits data...
		form = DocumentForm(request.POST, request.FILES)
                form.fields['system_name'].queryset=system.objects.filter(user=request.user)
                if form.is_valid():
			us=User.objects.get(username=request.user.username)
			c=form.cleaned_data
                        systems=system.objects.get(system=c['system_name'])
			data_raw=request.FILES['docfile'].read()
                        try: #Check that he submits a valid JSON
                                data=json.loads(data_raw)
                        except:
                                mes="Error during decoding JSON. Valid JSON object? "
                                log=upload_information(user=us, system=systems, test_id=active, timestamp=datetime.now(), comment=mes).save()
                                return render_to_response('Task2a.html',{"tests":tests, "current_test":active, "errors":errors, 'form': form, 'error':[mes], "attempts":attempts}, RequestContext(request))
			if not len(data['documents'])==active.number_of_abstracts:
                                mes="Different number of articles between the JSON and the test set. Check and try again!"
                                log=upload_information(user=us, system=systems, test_id=active, timestamp=datetime.now(), comment=mes).save()
                                return render_to_response("Task2a.html", {"tests":tests, "current_test":active, "errors":errors, 'form': form, 'error':[mes], "attempts":attempts}, RequestContext(request))	
			for doc in data['documents']: #Check that the PMIDs he is submitted actually belong to the current test set
                                try:
                                        entry=test_result(system=systems, test_id=active, pmid=Article.objects.get(pmid=doc['pmid']), mesh="D005260")
                                except:
                                        mes="Error while saving data for article with PMID: %d. Check that the PMID is in the active testset.\n\n" %int(doc['pmid'] )
                                        log=upload_information(user=us, system=systems, test_id=active, timestamp=datetime.now(), comment=mes).save()
                                        return render_to_response("Task2a.html", {"tests":tests, "current_test":active, "errors":errors, 'form': form, 'error':[mes], "attempts":attempts}, RequestContext(request))
			pt="/home/bioasq/public_html/webexample/uploads/documents/testset%d/%s.json" %(active.test_id, systems.system)
                        try:
                                f=open(pt, 'w')
                                myfile=File(f)
                                print>>myfile, data_raw
                                myfile.close()
                        except:
                                mes="Error while saving the file. Try again later."
                                log=upload_information(user=us, system=systems, test_id=active, timestamp=datetime.now(), comment=mes).save()
                                return render_to_response('Task2a.html',{"tests":tests, "current_test":active, "errors":errors, 'form': form, 'error':[mes], "attempts":attempts}, RequestContext(request))
			if test_result_file.objects.filter(system=systems).filter(test_id=active):
				entry2=test_result_file.objects.filter(system=systems).filter(test_id=active).delete()
				mes="There were old results saved for the system you selected; they were deleted.\n"
                        entry2=test_result_file(system=systems, user=us,  test_id=active, path=pt, timestamp=datetime.now()).save()
                        mes+="The new results were saved successfully.\n"
                        log=upload_information(user=us, system=systems, test_id=active, timestamp=datetime.now(), comment=mes).save()
                        return render_to_response('Task2a.html',{"tests":tests, "current_test":active, "errors":errors, 'form': form,'error':[mes], "attempts":attempts}, RequestContext(request))
	else:
		form = DocumentForm()
	        form.fields['system_name'].queryset=system.objects.filter(user=request.user)
	return render_to_response('Task2a.html',{"tests":tests, "current_test":active, "errors":errors, 'form': form,'error':[mes], "attempts":attempts}, RequestContext(request))




# Task 1A view, and upload a file functionality
#The user selects the file, the files is read and saved to the database.
#ATTENTION: No file is saved
@login_required
def task1a(request):
	error=[]
	errors=[]
	tests=Detail.objects.filter(test_id__lte=40).order_by('test_id')
	test=Detail.objects.filter(finished__gte=datetime.now()).filter(test_id__lte=40)
	attempts=test_result_file.objects.filter(user=request.user)

	if test:
		test=Detail.objects.get(finished__gte=datetime.now())
		testset=test.test_id
		current_test=test
		
	else:
		current_test=None
		testset=[]	
				
	
	if request.method=='POST': #If the user submits data...
		form = DocumentForm(request.POST, request.FILES)
		form.fields['system_name'].queryset=system.objects.filter(user=request.user)
		if form.is_valid():
			if not testset: #Check that there is active test set to save the results for
				error.append('There is no active test set to upload results.')
				form = DocumentForm()
				form.fields['system_name'].queryset=system.objects.filter(user=request.user)
				return render_to_response('Task1a.html',{"tests":tests, "errors":errors,  'form': form, 'error':error }, RequestContext(request))	
			
			us=User.objects.get(username=request.user.username)
			testset1=Detail.objects.get(test_id=testset)
			c=form.cleaned_data
			systems=system.objects.get(system=c['system_name'])
			mes=""		
			
			data_raw=request.FILES['docfile'].read()
			try:
				data=json.loads(data_raw)			
			except ValueError:
				mes+="Error during decoding JSON. Valid JSON object? "
				error.append(mes)
				log=upload_information(user=us, system=systems, test_id=testset1, timestamp=datetime.now(), comment=mes).save()
				return render_to_response('Task1a.html',{"tests":tests, "current_test":current_test, "errors":errors, 'form': form, 'error':error }, RequestContext(request))
			if not len(data['documents'])==current_test.number_of_abstracts:
				mes+="Different number of articles between the JSON and the test set. "
				error.append("The total number of the documents for which you are trying to upload ansers is not the same with the total number of the documents in the current test set. Add results in the JSON for every document in the active test set and try again.")
				log=upload_information(user=us, system=systems, test_id=testset1, timestamp=datetime.now(), comment=mes).save()
				return render_to_response("Task1a.html", {"tests":tests, "current_test":current_test, "errors":errors, 'form': form, 'error':error, "attempts":attempts }, RequestContext(request))

			#documents = test_result.objects.filter(system=systems).filter(test_id=testset) #Check if the user has uploaded answers for the test previously
                       #if documents:
                       #         documents.delete()
                       #         mes+="You had previously uploaded results for the testset %d, and they were erased. " % testset1.test_id

			for i in range(len(data['documents'])):
				for j in range(len(data['documents'][i]['labels'])):
					try:
						entry=test_result(system=systems, test_id=testset1, pmid=Article.objects.get(pmid=data['documents'][i]['pmid']), mesh=data['documents'][i]['labels'][j])				
				#		entry.save()
					except:
						mes+="Error while saving data from article with PMID: %d. Check that the PMID is in the testset and the MeSH you provided for the article are valid MeSH terms, e.g. 'D005260'. " %int(data['documents'][i]['pmid'])
					#	try:
					#		doc=test_result.objects.filter(system=systems).filter(test_id=testset)
					#		doc.delete()
					#		mes+="The results that were saved up to the error were deleted. "
					#	except: 
					#		mes+="The results that were saved up to the error were not deleted. "
						error.append(mes)
						log=upload_information(user=us, system=systems, test_id=testset1, timestamp=datetime.now(), comment=mes).save()
						return render_to_response('Task1a.html',{"tests":tests,"attempts":attempts, "current_test":current_test, "errors":errors, 'form': form, 'error':error }, RequestContext(request))  
				
			pt="/home/bioasq/public_html/webexample/uploads/documents/testset%d/%s.json" %(testset, systems.system)

			try:
				f=open(pt, 'w')
				myfile=File(f)
				print>>myfile, data_raw
				myfile.close()
			except:
				mes+="Error while saving the file. Try again later."
				error.append(mes)
				log=upload_information(user=us, system=systems, test_id=testset1, timestamp=datetime.now(), comment=mes).save()
				return render_to_response('Task1a.html',{"tests":tests,"attempts":attempts, "current_test":current_test, "errors":errors, 'form': form, 'error':error }, RequestContext(request))	

			entry2=test_result_file.objects.filter(system=systems).filter(test_id=testset1).delete()
			entry2=test_result_file(system=systems, user=us,  test_id=testset1, path=pt, timestamp=datetime.now()).save()
			mes+="The new results were saved successfully. "
			log=upload_information(user=us, system=systems, test_id=testset1, timestamp=datetime.now(), comment=mes).save()
			error.append(mes)
			return render_to_response('Task1a.html',{"tests":tests, "current_test":current_test, "errors":errors, 'form': form,"attempts":attempts, 'error':error }, RequestContext(request))
	form = DocumentForm()
	form.fields['system_name'].queryset=system.objects.filter(user=request.user)
	return render_to_response('Task1a.html',{"tests":tests, "current_test":current_test,"attempts":attempts, "errors":errors, 'form': form, 'error':error }, RequestContext(request))



@staff_member_required
def sendMessageToList(request):
	if request.method == 'POST':
		form=sendMessage(request.POST)
		if form.is_valid():
			c=form.cleaned_data
			receivers=User.objects.filter(user_profile__receive_information=True)
			for receiver in receivers:
                               msg=EmailMessage(c['subject'], c['message'], c['sender'], to=[receiver.email])
                               msg.send()
			message="The message has been sent to the receivers"
			#try:
			#	msg=EmailMessage(c['subject'], c['message'], c['sender'], to=['geompalik@hotmail.com']).send()
			#	message="The message has been sent!"
			#except:
			#	message="The message has not been sent!"
			return render_to_response('sendMessage.html', {'form':form, "message":message}, RequestContext(request))
        else:
                form=sendMessage()
        return render_to_response('sendMessage.html', {'form':form}, RequestContext(request))	


	
#Create test set, using the TI webservice.
@login_required
def create_tests(request):
	if request.method == 'POST':
		form=createTestForm(request.POST)
	
		if form.is_valid():
			c=form.cleaned_data
			pagination=0
			url="http://www.gopubmed.org/web/gopubmedbeta/bioasq/pubmedlucene"
			#f=open("/home/bioasq/public_html/webexample/dataa.txt").read()
			#qqq=json.loads(f)
			lista=[]
			for a in Article.objects.all():
				lista.append(str(a.pmid))
			lista.extend(['25159766', '25159765'])
			ss=",".join(lista)
			message=""
			removed=[]
			while 1:
				data={"getCitationAfterDateWithoutMesh":[c['starting_date'], pagination, 1000, lista]}
				data={"json":json.dumps(data).encode('utf-8')}
				s=requests.Session()
				tmplink=s.get("http://www.gopubmed.org/web/gopubmedbeta/bioasq/pubmed")
				res=s.post(tmplink.text, data=data)
				d=json.loads(res.text)
				if "exception" in d:
					break
				if pagination==0:	
					entry=Detail(test_id=c["test_id"], started=c['started'], finished=c['finished'], downloaders='[]')
					entry.save()
					distro=Detail.objects.get(started=c['started'])
					lis=[]
					sys=system.objects.get(system="bioasq_baseline")
				
				for i in range(len(d['result']['documents'])):
					entry2=Article(distro=Detail.objects.get(started=c['started']), pmid=d['result']['documents'][i]['pmid'], title=d['result']['documents'][i]['title'], abstract=d['result']['documents'][i]['documentAbstract'])
					entry2.save()
					list_bio=[]
					dictio={}
					for k in range(len(d['result']['documents'][i]['meshAnnotations'])):
						list_bio.append(d['result']['documents'][i]['meshAnnotations'][k]['uri']['id'])
					dictio={"pmid":int(d['result']['documents'][i]['pmid']), 'labels':list_bio }
					lis.append(dictio)
				params={"fromDate":c['starting_date'], "page":pagination, "articlesPerPage":1000,"pmids":ss}				
				r=requests.post(url, data=params)
				pt_zip_extract="/home/bioasq/public_html/webexample/uploads/media/Zips/extracted/Zip%d" %pagination
				removed.append(pt_zip_extract)
				z = zipfile.ZipFile(StringIO.StringIO(r.content))
				z.extractall(pt_zip_extract) 
				z.close()
				pagination+=1
			entry=Detail.objects.get(started=c['started'])
			final_dictio={'documents':lis}
			ddd=json.dumps(final_dictio)
			pt="/home/bioasq/public_html/webexample/uploads/documents/testset%d/bioasq_baseline.json" %entry.pk
			f=open(pt, 'w')
			myfile1=File(f)
			print>>myfile1, ddd
			myfile1.close()
			test_result_file(system=sys, user=User.objects.get(username="bioasq"),  test_id=entry, path=pt, timestamp=datetime.now()).save()
			pt="/home/bioasq/public_html/webexample/uploads/media/raw_testset%d.txt" %entry.pk
			pt2="/home/bioasq/public_html/webexample/uploads/media/vectorized_testset%d.zip" %entry.pk
			entry.path_raw=pt
			entry.path_vect=pt2
			#name="vecrorized_testset%d.zip" %entry.pk
			entry.number_of_abstracts=len(Article.objects.filter(distro=entry))
			entry.save()
			
			#Create the file

			d=Article.objects.filter(distro=entry)
			d=json.dumps({"documents":TestSerializer(d).data})
			f=open(pt, 'w')
			myfile=File(f)
			print>>myfile, d
			myfile.close()
			


			#Create the zip
			subprocess.call(["java", "-jar", "/home/bioasq/public_html/webexample/merger.jar", "/home/bioasq/public_html/webexample/uploads/media/Zips/extracted/", "/home/bioasq/public_html/webexample/uploads/media/vectorized2"])
			path="/home/bioasq/public_html/webexample/uploads/media/vectorized2"
			zip_f=zipfile.ZipFile(pt2, "w")
			for f in listdir(path):
				zip_f.write(os.path.join(path, f), f)
			zip_f.close()
			try:
				for fold in removed:
					shutil.rmtree(fold)
			except:
				pass
			path_to_delete="/home/bioasq/public_html/webexample/uploads/media/vectorized2"
                        for f in listdir(path_to_delete):
                                os.remove(os.path.join(path_to_delete,f))

			

			form=createTestForm()

			#Send the e-mails to the users.
			#subject="BioASQ-New test set available"
			#message = render_to_string('sendmail.txt', {"detail":entry})
			#receivers=User.objects.filter(user_profile__receive_information=True)
			#for receiver in receivers:
			#	msg=EmailMessage(subject, message, 'admin@bioasq.org', to=[receiver.email])
			#	msg.send()
			return render_to_response('create_test.html', {'form':form, "message":"The new test set has been created and users have been notified!"}, RequestContext(request))
	else:	
		form=createTestForm()
		return render_to_response('create_test.html', {'form':form}, RequestContext(request))

def deleter(request):
	import shutil
	tank=['/home/bioasq/public_html/webexample/uploads/media/Zips/extracted', '/home/bioasq/public_html/webexample/uploads/media/Zips/extracted/Zips/Zips/Zips/Zip2',]
	shutil.rmtree(tank[0])
	#for f in listdir('/home/bioasq/public_html/webexample/uploads/media/Zips/extracted/Zips/Zips/Zips/Zip1'):
	#	os.remove(os.path.join('/home/bioasq/public_html/webexample/uploads/media/Zips/extracted/Zips/Zips/Zips/Zip1', f))
	return HttpResponse("Done!")      	
	

def contactview(request):
	if request.method=="POST":
		result=check_captcha(request)
		if result.is_valid:
			subject=request.POST.get('topic', '')
			message=request.POST.get('message', '')
			from_email=request.POST.get('email', '')
			if subject and message and from_email:
				try:
					send_mail(subject, message, from_email, ['geompalik@hotmail.com'])
				except BadHeaderError:
					return HttpResponse('Invalid header found.')
				return HttpResponseRedirect('/contact/thankyou/')
			else:
				form=ContactForm()
				public_key="6LfOBd4SAAAAAKJMafi8I7-wMtr6M65wtCVKhD71"
				script=displayhtml(public_key=public_key)
				return render_to_response('contacts.html', {'form':form,'script':script}, context_instance=RequestContext(request))
		#return render_to_response('contacts.html', {'form': ContactForm()}, RequestContext(request))
	form=ContactForm()
	public_key="6LfOBd4SAAAAAKJMafi8I7-wMtr6M65wtCVKhD71"
	script=displayhtml(public_key=public_key)
	return render_to_response('contacts.html', {'form':form,'script':script}, context_instance=RequestContext(request))





#Render the page for profile editing
@login_required
def profile_edit(request):
	instance=User.objects.get(username=request.user.username)
	formSystem=add_system()
	formEmail=email_change_form(instance=instance)
	instance_profile=user_profile.objects.get(user=instance)
	formProfile=task_selection_edit_form(instance=instance_profile)
	return render_to_response('profile.html', {'formSystem':formSystem, 'formEmail':formEmail, 'formProfile':formProfile, "systems":system.objects.filter(user=instance)}, RequestContext(request))



#Change the e-mail of a user
@login_required
def email_change(request):
	instance=User.objects.get(username=request.user.username)
	if request.method == "POST":
		form = email_change_form(data=request.POST, instance=instance)
		if form.is_valid():
			form.save()
			return render_to_response('email_changed.html', {"message":"e-mail"}, RequestContext(request) )
	else:
		form=email_change_form(instance=instance)
	return render_to_response('email_change_form.html', {'form':form, "message":"the system descriptions"}, RequestContext(request))		

def email_changed(request):
	return render_to_response('email_changed.html', {"message":"e-mail"}, RequestContext(request))


@login_required	
def add_a_new_system(request):
	instance=User.objects.get(username=request.user.username)
	if request.method=="POST":
		form=add_system(request.POST)
		if form.is_valid():
			c=form.cleaned_data
			if  len(system.objects.filter(user=instance))<5:
				try:
					entry=system(user=instance, system=c["system_name"], system_description=c["system_description"])
					entry.save()
					mes="The new system has been added successfully!"
				except:
					mes="Error while saving the 'System name' and the 'System Description'. They are already in use."
				form=add_system()
				return render_to_response('add_system.html', {'form':form, "message":mes, "systems":system.objects.filter(user=instance)}, RequestContext(request))
			else:
				form=add_system()
				mes="You have already registered 5 systems. You can not register more."
				return render_to_response('add_system.html', {'form':form, "message":mes, "systems":system.objects.filter(user=instance)}, RequestContext(request))
	else:
		form=add_system()
		return render_to_response('add_system.html', {'form':form, "systems":system.objects.filter(user=instance)}, RequestContext(request))		
				
				
		
		
	
#change the options (checkboxes) the user has put during registration.
@login_required
def task_selection_edit(request):
	instance=User.objects.get(username=request.user.username)
	instance=user_profile.objects.get(user=instance)
	if request.method == "POST":
		form =task_selection_edit_form(data=request.POST, instance=instance)
		if form.is_valid():
			form.save()
			return render_to_response('email_changed.html', {"message":"selection regarding the tasks you will participate"}, RequestContext(request) )
	else: 
		form=task_selection_edit_form(instance=instance)
		return render_to_response('email_change_form.html', {'form':form, "message":"the tasks you are going to participate"}, RequestContext(request))



def results(request):
	tests=Detail.objects.filter(test_id__gte=1).filter(test_id__lte=19)
	length=[]
	evaluated=[]
	i=0
	dd={}
	for test in tests:
		try:
			dd[i]="%d(%d)"%(test.number_of_abstracts, test.number_of_abstracts_annotated)
		except:
			dd[i]="%d(%d)"%(test.number_of_abstracts, 0)
		i+=1		
		
	evaluation=eval_meas.objects.all()
	return render_to_response('results2.html', {"tests":tests, "evaluation":evaluation, "p":dd }, RequestContext(request))

def results_additional_1a(request):
	tests=Detail.objects.filter(test_id__gte=20).filter(test_id__lte=40)
	evaluation=eval_meas.objects.all()
	return render_to_response('additional_results_1a.html', {"tests":tests, "evaluation":evaluation}, RequestContext(request))

def results2a(request):
        tests=Detail.objects.filter(test_id__gte=41)
        evaluation=eval_meas.objects.all()
	dd={(x.test_id-41):"%d (%d)"%(x.number_of_abstracts, x.number_of_abstracts_annotated) for x in Detail.objects.filter(test_id__gte=42).filter(test_id__lte=56)}
        return render_to_response('results2a.html', {"tests":tests, "evaluation":evaluation, "p":dd}, RequestContext(request))

@staff_member_required	
def evaluate(request):
	#For every testset that has been released...
	#lines=open('/home/bioasq/public_html/webexample/name_id_mapping2013.txt', 'r').read().splitlines()
	lines=open('/home/bioasq/public_html/webexample/name_id_mapping.txt', 'r').read().splitlines()
	c=dict(line.split("=") for line in lines)
	web_service_progress=[]
	web_service_progress.append("Initializing..\n")
	ttt,CNT= [],0
	#qu=Detail.objects.filter(test_id__lte=6).filter(test_id__gte=6)
	qu=Detail.objects.filter(test_id__gte=57) #it was 40
	#qu=Detail.objects.filter(test_id__lte=56).filter(test_id__gte=56)
	#ttt.append(qu)
	for testset in reversed(qu):
	#for testset in Detail.objects.all():
		#For the particular testset, select the PMIDs
		#with open('/home/bioasq/public_html/webexample/test%dpmids' %testset.test_id, 'r') as input: #HERE
		#	pmid_list=json.load(input) #HERE
		pmid_list=[] 
		for article in Article.objects.filter(distro=testset): 
			pmid_list.append(str(article.pmid)) 
		data={"getMajorMeshFor":[pmid_list]}	
		data={"json":json.dumps(data).encode('utf-8')}
		s=requests.Session()
		tmplink=s.get("http://www.gopubmed.org/web/gopubmedbeta/bioasq/pubmed")
		#Ask for the MeSH for every article in the test set
		res=s.post(tmplink.text, data=data)
		d=json.loads(res.text)

		if len(d['result'])<0.05*testset.number_of_abstracts:
			web_service_progress.append("The web service didn't return enough results for the test set %d!. It returned %d.  The measures were initialized with zeros." %(testset.test_id, len(d['result'])))
			for sys in system.objects.all():
				flag=test_result_file.objects.filter(system=sys).filter(test_id=testset)
				if flag:
					eval_meas.objects.filter(user=sys).filter(test_id=testset).delete()
					eva=eval_meas(user=sys, test_id=testset, accuracy=float(-1), ebp=float(-1), example_based_recall=float(-1), example_based_f=float(-1), macro_precision=float(-1), macro_recall=float(-1), macro_f_measure=float(-1), micro_precision=float(-1), micro_recall=float(-1), micro_f=float(-1), hierarchical_precision=float(-1), hierarchical_recall=float(-1), hierarchical_f=float(-1), lca_p=float(-1), lca_r=float(-1), lca_f=float(-1)).save()	
			continue
		else:
			web_service_progress.append("The web service returned staff for the test set %d!\nI am starting the process.." %testset.test_id)
			testset.number_of_abstracts_annotated=len(d['result'])
			testset.save()
		pmid_list=[]
		#editFileFlat=open("/home/bioasq/public_html/webexample/uploads/media/editFile%d.txt" %testset.test_id, 'w')
		#editFileHier=open("/home/bioasq/public_html/webexample/uploads/media/editFileHier%d.txt" %testset.test_id, 'w')
		#editMYFile=File(editFileFlat)
		#print>>editMYFile, "starting.."
		#editHier=File(editFileHier)		
		#print>>editHier, "starting.."
		f=open("/home/bioasq/public_html/webexample/uploads/media/true_labels.txt", 'w')
		myfile=File(f)
		#Check for which PMIDs you received MeSH
		for i in range(len(d['result'])):
			pmid_list.append(d['result'][i]['pmid'])
			string=""
			#For each one of the PMIDs collect the MeSH
			for j in range(len(d['result'][i]["majorMesh"])):
				try:
					string+=c[str(d['result'][i]["majorMesh"][j])] #Normally, this should be in indexes, but the web service returns HUMAN WORDS
					string+=" "
				except:
					CNT+=1
			#string+="\n"
			print>>myfile, string #Save the result in a file, where each line is an article (pmid-list)
				
		myfile.close()
		with open('/home/bioasq/public_html/webexample/pmidsOfficialTask2a/pmids_testset%d'%testset.test_id, 'w') as out:
			json.dump(pmid_list, out, indent=2)
		#Make the Golden File you have just created in the format that is used during evaluation.
		subprocess.call(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "converters.MapMeshResults", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mapping.txt", "/home/bioasq/public_html/webexample/uploads/media/true_labels.txt", "/home/bioasq/public_html/webexample/uploads/media/golden_labels.txt"])
		#After having the golden, try for each user..
		ss=[]
		#ss.append(system.objects.get(system="mc2"))
		for sys in system.objects.all():
			#if the user has uploaded things about this particular test set, try to evaluate him.
			flag=test_result_file.objects.filter(system=sys).filter(test_id=testset)
			if flag:
				g=open(flag[0].path)
				userData=json.loads(g.read())
				string=""
				f=open("/home/bioasq/public_html/webexample/uploads/media/system_A_results.txt", 'w')
				myfile=File(f)
				for i in range(len(pmid_list)):
					try:
						q=[element for element in userData['documents'] if int(element['pmid'])==int(pmid_list[i])][0]
					except:
						messages="This system had problem during evaluation in the testset, while trying to find the results for the pmid: %s" %pmid_list[i]
						log=upload_information(user=User.objects.get(username="bioasq"), system=sys, test_id=testset, timestamp=datetime.now(), comment=messages).save()
						break		
					string=""
					
					for k in range(len(q['labels'])):
						if q['labels'][k] in c.values():
							string+=q['labels'][k]
							string+=" "
					if string=="":
						string="D006801"
					print>>myfile, string
				myfile.close()		
				#Edw metatrepw auta tou sistimatos pros eksetasi
				subprocess.call(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "converters.MapMeshResults", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mapping.txt", "/home/bioasq/public_html/webexample/uploads/media/system_A_results.txt", "/home/bioasq/public_html/webexample/uploads/media/system_results_mapped.txt"])
				#I need to run for the flat measures
				result=subprocess.Popen(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "evaluation.Evaluator", "/home/bioasq/public_html/webexample/uploads/media/golden_labels.txt", "/home/bioasq/public_html/webexample/uploads/media/system_results_mapped.txt"], stdout=subprocess.PIPE)
				p=result.communicate()
				arr=p[0].split() #this is string and I am spliting it...
				
				#Otan to kalw epanaliptika, enimerwnei i dimiourgei allo? Dimiourgei allo. Alla twra einia ok
				result=subprocess.Popen(["/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/hierarchical/bin/HEMKit", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mesh_hier_int.txt", "/home/bioasq/public_html/webexample/uploads/media/golden_labels.txt", "/home/bioasq/public_html/webexample/uploads/media/system_results_mapped.txt", "4", "5"], stdout=subprocess.PIPE)
				s=result.communicate()
				w=s[0].split()
				eval_meas.objects.filter(user=sys).filter(test_id=testset).delete()
				try:
					evals=eval_meas(user=sys, test_id=testset, accuracy=float(arr[0]), ebp=float(arr[1]), example_based_recall=float(arr[2]), example_based_f=float(arr[3]), macro_precision=float(arr[4]), macro_recall=float(arr[5]), macro_f_measure=float(arr[6]), micro_precision=float(arr[7]), micro_recall=float(arr[8]), micro_f=float(arr[9]), hierarchical_precision=float(w[0]), hierarchical_recall=float(w[1]), hierarchical_f=float(w[2]), lca_p=float(w[3]), lca_r=float(w[4]),lca_f=float(w[5])).save()
					#listing="%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  " %(sys.system, arr[0], arr[1], arr[2], arr[3], arr[4], arr[5],arr[6],arr[7],arr[8],arr[9])
					#listing_hier="%s, %s, %s, %s, %s, %s, %s" %(sys.system, w[0], w[1], w[2],w[3],w[4],w[5])
					#print>>editMYFile, listing
					#print>>editHier, listing_hier
				except:
					eva=eval_meas(user=sys, test_id=testset, accuracy=float(0), ebp=float(0), example_based_recall=float(0), example_based_f=float(0), macro_precision=float(0), macro_recall=float(0), macro_f_measure=float(0), micro_precision=float(0), micro_recall=float(0), micro_f=float(0), hierarchical_precision=float(0), hierarchical_recall=float(0), hierarchical_f=float(0), lca_p=float(0), lca_r=float(0), lca_f=float(0)).save()
					log=upload_information(user=User.objects.get(username="bioasq"), system=sys, test_id=testset, timestamp=datetime.now(), comment="This system had problem during evaluation in the testset").save()
				os.remove("/home/bioasq/public_html/webexample/uploads/media/system_results_mapped.txt")
				os.remove("/home/bioasq/public_html/webexample/uploads/media/system_A_results.txt")
		os.remove("/home/bioasq/public_html/webexample/uploads/media/golden_labels.txt")
		os.remove("/home/bioasq/public_html/webexample/uploads/media/true_labels.txt")
		#editMYFile.close()
		#editHier.close()
		web_service_progress.append('CNT: %d' %CNT)
	return render_to_response('email_changed.html', {"message2":web_service_progress}, RequestContext(request))



