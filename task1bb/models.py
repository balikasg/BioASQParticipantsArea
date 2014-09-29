from django.db import models
from task1b.models import *
from django.contrib.auth.models import User
from Test.models import * 
from datetime import datetime

class user_results_1bb(models.Model):
	user=models.ForeignKey(User)
	system=models.ForeignKey(system)
	test_id=models.ForeignKey(Detail1b)
	path=models.CharField(max_length=300)
	datetime=models.DateTimeField(default=datetime.now())
	class Meta:
		verbose_name="Test Result file for 1B, phase B"
		verbose_name_plural=verbose_name



class evaluation_measures_1bb(models.Model):
        testset=models.ForeignKey(Detail1b)
        system=models.ForeignKey(system)
	acc=models.FloatField(null=True, blank=True, verbose_name="yes/no: accuracy")
	s_acc=models.FloatField(null=True, blank=True, verbose_name="factoid: strict accuracy")
	l_acc=models.FloatField(null=True, blank=True, verbose_name="factoid: lenient accuracy")
	mrr=models.FloatField(null=True, blank=True, verbose_name="factoid: MRR")
	prec=models.FloatField(null=True, blank=True, verbose_name="list: mean precision")
	rec=models.FloatField(null=True, blank=True, verbose_name="list: mean recall")	
	fmeas=models.FloatField(null=True, blank=True, verbose_name="list: f measure")
	r2p=models.FloatField(null=True, blank=True, verbose_name="ROUGE2: precision")
	r2r=models.FloatField(null=True, blank=True, verbose_name="ROUGE2: recall")
	r2f=models.FloatField(null=True, blank=True, verbose_name="ROUGE2: f measure")
	r4p=models.FloatField(null=True, blank=True, verbose_name="ROUGE-SU4: precision")
	r4r=models.FloatField(null=True, blank=True, verbose_name="ROUGE-SU4: recall")
	r4f=models.FloatField(null=True, blank=True, verbose_name="ROUGE-SU4: f measure")
	read=models.FloatField(null=True, blank=True, verbose_name="Readability")
	recall=models.FloatField(null=True, blank=True, verbose_name="Recall")
	rep=models.FloatField(null=True, blank=True, verbose_name="Repetition")
	preci=models.FloatField(null=True, blank=True, verbose_name="Precision")
	class Meta:
                verbose_name="Evaluation measures for 1B, phase B"
                verbose_name_plural=verbose_name




