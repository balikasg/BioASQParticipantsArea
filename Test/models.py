from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Detail(models.Model):
	test_id=models.IntegerField(primary_key=True)	
	started=models.DateTimeField()
	finished=models.DateTimeField()
	number_of_abstracts=models.IntegerField(null=True, blank=True)
	number_of_abstracts_annotated=models.IntegerField(null=True, blank=True)
	number_of_downloads=models.IntegerField(null=True, blank=True, default=0)
	number_of_abstracts_oracle=models.IntegerField(null=True, blank=True, default=0)
	path_raw=models.CharField(max_length=300, null=True, blank=True)
	path_vect=models.CharField(max_length=300, null=True, blank=True)	
	downloaders=models.TextField(null=True, blank=True)
	is_oracle=models.BooleanField(default=False)
	def __unicode__(self):
		return unicode(self.test_id)
        
class Article(models.Model):
	distro=models.ForeignKey(Detail)
	pmid=models.IntegerField(primary_key=True)
	title=models.CharField(null=True, blank=True, max_length=200)
	abstract=models.CharField(null=True, blank=True, max_length=10000)
	class Meta:
		ordering=['-pmid']
	def __unicode__(self):
		return unicode(self.pmid)
	
class bioasq_baseline(models.Model):
	distro=models.ForeignKey(Detail)
	pmid=models.ForeignKey(Article)
	mesh=models.CharField(max_length=7)

class user_profile(models.Model):
	user=models.ForeignKey(User, unique=True)
	institution=models.CharField(max_length=200)
	task1a=models.BooleanField()
	task1b1=models.BooleanField()
	task1b2=models.BooleanField()
	task2a=models.BooleanField()
	task2b=models.BooleanField()
	receive_information=models.BooleanField()
	class Meta:
		verbose_name="User Profile"
	
	def __unicode__(self):
		return u'%s %s' % (self.user, self.institution)

class system(models.Model):
	user=models.ForeignKey(User, verbose_name="the user that has the system")
	system=models.CharField(max_length=20, unique=True)
	system_description=models.CharField(max_length=20, unique=True, verbose_name="System Description")
	class Meta:
		verbose_name="Systems per User"
		verbose_name_plural=verbose_name
	def __unicode__(self):
		return u'%s' % (self.system)
	
class test_result(models.Model):
	#team_id=models.ForeignKey(User)
	system=models.ForeignKey(system)
	test_id=models.ForeignKey(Detail)
	pmid=models.ForeignKey(Article)
	mesh=models.CharField(max_length=7)
	class Meta:
		verbose_name="Test Result"
	



class test_result_file(models.Model):
	user=models.ForeignKey(User)
	system=models.ForeignKey(system)
	test_id=models.ForeignKey(Detail)
	path=models.CharField(max_length=300)
	timestamp=models.DateTimeField()
	class Meta:
		verbose_name="Test Result file"
		verbose_name_plural="Test Result files"




class upload_information(models.Model):
	user=models.ForeignKey(User)
	system=models.ForeignKey(system)
	test_id=models.ForeignKey(Detail)
	timestamp=models.DateTimeField()
	comment=models.CharField(max_length=200, null=True, blank=True)
	class Meta:
		verbose_name="Upload Information/Log"
		verbose_name_plural=verbose_name


		
class eval_meas(models.Model):
	user=models.ForeignKey(system, verbose_name="the participating system")
	test_id=models.ForeignKey(Detail, verbose_name="the related test set")
	accuracy=models.FloatField()
	ebp=models.FloatField(verbose_name="example based precision")
	example_based_recall=models.FloatField()
	example_based_f=models.FloatField(verbose_name="example based f-measure")
	macro_precision=models.FloatField()
	macro_recall=models.FloatField()
	macro_f_measure=models.FloatField(verbose_name="macro f-measure")
	micro_precision=models.FloatField()
	micro_recall=models.FloatField()
	micro_f=models.FloatField(verbose_name="micro f-measure")
	hierarchical_precision=models.FloatField()
	hierarchical_recall=models.FloatField()
	hierarchical_f=models.FloatField(verbose_name="hierarchical F-measure")
	lca_p=models.FloatField(verbose_name="lca Precision")
	lca_r=models.FloatField(verbose_name="lca Recall")
	lca_f=models.FloatField(verbose_name="lca F-measure")
	class Meta:
		verbose_name="Evaluation Measure"
		verbose_name_plural="Evaluation Measures"



