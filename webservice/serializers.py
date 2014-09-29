from Test.models import *
from rest_framework import serializers

class TestSerializer(serializers.ModelSerializer):
	class Meta:
		model=Article
		fields=('pmid', 'title', 'abstract')

class TestDistroSerializer(serializers.ModelSerializer):
	class Meta:
		model=Detail
		fields=('test_id', 'number_of_abstracts', 'started', 'finished')
		
		
class ResultSerializer(serializers.ModelSerializer):
	class Meta:
		model=test_result
		fields=('pmid', 'mesh')		

