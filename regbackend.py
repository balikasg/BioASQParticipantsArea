from Test.models import user_profile
from forms import *


def user_created(sender, user, request, **kwargs):
	form = UserRegForm(request.POST)
	data = user_profile(user=user)
	data.institution = request.POST.get("institution")
	data.task1a=request.POST.get("task1a", False)
	data.task1b1=request.POST.get("task1b1", False)
	data.task1b2=request.POST.get("task1b2", False)
	data.task2a=request.POST.get("task2a", False)
	data.task2b=request.POST.get("task2b",False)
	data.receive_information=request.POST.get("receive_information", False)
	data.save()

from registration.signals import user_registered
user_registered.connect(user_created)
