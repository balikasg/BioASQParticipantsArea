from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from Test.models import * 

# Create your models here.
class Detail1b(models.Model):
 	phase_choices=(('A', 'Phase A'),('B', 'Phase B'),)
	phase=models.CharField(max_length=1, choices=phase_choices, default="A")
	test_id=models.IntegerField(primary_key=False)
	started=models.DateTimeField()
	finished=models.DateTimeField()
	number_of_questions=models.IntegerField(null=True, blank=True)
	path=models.CharField(max_length=300, null=True, blank=True)
	golden_path=models.CharField(max_length=300, null=True, blank=True)
	number_of_downloads=models.IntegerField(null=True, blank=True, default=0)
	downloaders=models.TextField(null=True, blank=True)
	is_oracle=models.BooleanField(default=False)
	def __unicode__(self):
		return unicode(self.test_id)



class golden_question_1b(models.Model):
	question_id=models.CharField(max_length=40)
	body=models.TextField()
	type=models.CharField(max_length=7)
	concepts=models.TextField()
	documents=models.TextField()
	snippets=models.TextField()
	triples=models.TextField()
	exact_answer=models.TextField()
	ideal_answer=models.TextField()
	testset=models.ForeignKey(Detail1b)
	

class user_results_1b(models.Model):
	user=models.ForeignKey(User)
	system=models.ForeignKey(system)
	test_id=models.ForeignKey(Detail1b)
	path=models.CharField(max_length=300)
	datatime=models.DateTimeField(default=datetime.now())
	class Meta:
		verbose_name="Test Result file for 1B"
		verbose_name_plural="Test Result files for 1B"


class upload_information_for_1b(models.Model):
        user=models.ForeignKey(User)
        system=models.ForeignKey(system)
        test_id=models.ForeignKey(Detail1b)
        timestamp=models.DateTimeField()
        comment=models.CharField(max_length=200, null=True, blank=True)
        class Meta:
                verbose_name="Upload Information/Log for Task1b"
                verbose_name_plural=verbose_name


class evaluation_measures_1b(models.Model):
	testset=models.ForeignKey(Detail1b)
	user=models.ForeignKey(system)
	mp_con=models.FloatField(null=True, blank=True, verbose_name="concepts: mean precision")
	mr_con=models.FloatField(null=True, blank=True, verbose_name="concepts: recall")
	f_con=models.FloatField(null=True, blank=True, verbose_name="concepts: f-measure")
	MAP_con=models.FloatField(null=True, blank=True, verbose_name="concepts: MAP")
	GMAP_con=models.FloatField(null=True, blank=True, verbose_name="concepts: GMAP")
	mp_art=models.FloatField(null=True, blank=True, verbose_name="articles:mean precision")
	mr_art=models.FloatField(null=True, blank=True, verbose_name="articles:recall")
	f_art=models.FloatField(null=True, blank=True, verbose_name="articles:f-measure")
	MAP_art=models.FloatField(null=True, blank=True, verbose_name="articles: MAP")
	GMAP_art=models.FloatField(null=True, blank=True, verbose_name="articles:GMAP")
	mp_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: mean precision")
	mr_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: recall")
	f_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: f-measure")
	MAP_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: MAP")
	GMAP_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: GMAP")
	mp_trip=models.FloatField(null=True, blank=True, verbose_name="triples: mean precision")
	mr_trip=models.FloatField(null=True, blank=True, verbose_name="triples: recall")
	f_trip=models.FloatField(null=True, blank=True, verbose_name="triples: f-measure")
	MAP_trip=models.FloatField(null=True, blank=True, verbose_name="triples: MAP")
	GMAP_trip=models.FloatField(null=True, blank=True, verbose_name="triples: GMAP")

	class Meta:
		verbose_name="Evaluation Measure for Task 1b phase A"
		verbose_name_plural="Evaluation Measures for Task 1b phase A"





