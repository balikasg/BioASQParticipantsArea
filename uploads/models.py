from django.db import models
from django.contrib.auth.models import User
from Test.models import Detail

# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents')
    user=models.ForeignKey(User)
    test_set=models.ForeignKey(Detail)
    
