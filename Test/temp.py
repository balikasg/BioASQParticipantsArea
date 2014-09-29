# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from uploads.models import Document
from uploads.forms import DocumentForm
from Test.models import Detail

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        tests=Detail.objects.all()
        for test in tests:
			if test.is_active==True:
				testset=test.test_id
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'], user=User.objects.get(username=request.user.username), test_set=Detail.objects.get(test_id=testset))
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('uploads.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request))
