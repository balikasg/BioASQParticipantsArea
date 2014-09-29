# Create your views here.
from django.core.files import File
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from Test.models import *
from webservice.serializers import *
from rest_framework import permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from Test.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
from datetime import datetime


class test_list(generics.ListAPIView):
	"""
	Retrieve the available test sets.
	"""	
	model=Detail
	serializer_class=TestDistroSerializer
	permission_classes = (permissions.IsAuthenticated,)
	
	
class article_list(APIView):
	"""
	Retrieve all the articles of a test set.
	"""	
	permission_classes = (permissions.IsAuthenticated, )
	def get(self, request, pk, format=None):
		try:
		
			pk=int(pk)
			pk+=41
			target=Detail.objects.get(test_id=pk)
			target.number_of_downloads+=1
			downs=json.loads(target.downloaders)
		        downs.append(request.user.username)
        		target.downloaders=json.dumps(downs)
			target.save()
			serializer=TestSerializer(Article.objects.filter(distro=Detail.objects.get(test_id=pk)))
			return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			return Response("An error occured. You may have submitted an invalid integer e.g. string or the integer you submitted does not correspond to a BioASQ test set.")


@csrf_exempt
def results1(request, pk):
	"""
	Post the results for a test set from task A
	"""
	if request.method=="POST":
		mes=""
		if Detail.objects.filter(finished__gte=datetime.now()): #Make sure there is an active test set
			test=Detail.objects.get(finished__gte=datetime.now())
		else:
			return HttpResponse("Currently, there is no test set active, in order to upload your results!\n\n")
		try: #Make sure he posted a number as testset indicator and not a string for example
			distro=int(pk)+41
		except:
			return HttpResponse("Error when processing the integer that corresponds to the active test set in the URL. Confirm that it is indeed an integer and try again.\n\n")
		if not test.test_id == distro: #Make sure that the number corresponds to the active test set
			return HttpResponse("The integer you provided in the URL doesn't match the id of the currently active test set. For example, to submit results for the Week 2 test set of the first batch you should  make the POST request http://bioasq.lip6.fr/tests/2/. Check and try again. The currently active id is %d.\n\n" %int(test.test_id-41))
		try: #Make sure he posted a valid JSON
			data_raw=request.raw_post_data
			data=json.loads(data_raw)
		except:
			return HttpResponse("Error during decoding JSON. Valid JSON object?\n\n")
		user=authenticate(username=data['username'], password=data['password']) #Is he a BioASQ user?
		if user is not None: #Call authenticate method to check if user is real
			user1=User.objects.get(username=data['username'])
			sys=system.objects.filter(user=user1).get(system=data["system"])
			if not sys:
				return HttpResponse("The system name you provided does not belong to you. Check and try again!\n\n")
			if not len(data['documents'])==test.number_of_abstracts:
				mes+="The total number of the documents for which you are trying to upload ansers is not the same with the total number of the documents in the current test set. Add results in the JSON for every document in the active test set and try again.\n\n"
				log=upload_information(user=user1, system=sys, test_id=test, timestamp=datetime.now(), comment=mes).save()
				return HttpResponse(mes)

			for doc in data['documents']:
				try: 
					entry=test_result(system=sys, test_id=test, pmid=Article.objects.get(pmid=doc['pmid']), mesh="D005260")
				except:
					mes+="Error while saving data for article with PMID: %d. Check that the PMID is in the active testset.\n\n" %int(doc['pmid'] )
					log=upload_information(user=user1, system=sys, test_id=test, timestamp=datetime.now(), comment=mes).save()
					return HttpResponse(mes)
			flag=test_result_file.objects.filter(system=sys).filter(test_id=test)
			if flag:#Check if he has submitted results for the same test set and same system and delete them.
                                flag.delete()
                                mes+="You had already uploaded some results for this testset and they were deleted.\n"
			pt="/home/bioasq/public_html/webexample/uploads/documents/testset%d/%s.json" %(test.test_id, sys.system)
			try:
				f=open(pt, 'w')
				myfile=File(f)
				print>>myfile, data_raw
				myfile.close()
			except:
				mes+="Error while saving the file. Try again later."
				log=upload_information(user=user1, system=sys, test_id=test, timestamp=datetime.now(), comment=mes).save()
				return HttpResponse(mes)

                        entry2=test_result_file(system=sys, user=user1,  test_id=test, path=pt, timestamp=datetime.now()).save()
			mes+="The new results were saved successfully.\n\n "					
			log=upload_information(user=user1, system=sys, test_id=test, timestamp=datetime.now(), comment=mes).save()
			return HttpResponse(mes)
		else: 
			return HttpResponse("There was a problem during your authentication. Please, check your username and your password! \n")
	else:
		return HttpResponse("You need to use the 'POST' method in your Http Request.")
