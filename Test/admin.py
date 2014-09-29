from django.contrib import admin
from Test.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from Test.models import user_profile




#Enabling User Profile 
admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
	model = user_profile
    
class UserProfileAdmin(UserAdmin):
	inlines = [ UserProfileInline, ]
admin.site.register(User, UserProfileAdmin)
###################################################

class bioasq_baseline_model(admin.ModelAdmin):
        list_display=('pmid', 'mesh')
admin.site.register(bioasq_baseline, bioasq_baseline_model)
	
class test_result_model(admin.ModelAdmin):
	list_display=('system', 'test_id', 'pmid', 'mesh')
admin.site.register(test_result, test_result_model)	

class test_result_file_model(admin.ModelAdmin):
	list_display=('user', 'system', 'test_id', 'path')
admin.site.register(test_result_file, test_result_file_model)


class log_admin(admin.ModelAdmin):
	list_display=('user', 'system', 'test_id', 'timestamp', 'comment')
admin.site.register(upload_information, log_admin)

class measures_admin(admin.ModelAdmin):
	list_display=('user', 'test_id')
admin.site.register(eval_meas, measures_admin)

class systems_admin(admin.ModelAdmin):
	list_display=('user', 'system', 'system_description')
admin.site.register(system, systems_admin)
	
class MyModel(admin.ModelAdmin):
	list_display=('test_id',  "finished","number_of_abstracts",'number_of_abstracts_annotated','number_of_downloads', 'path_raw','path_vect')
admin.site.register(Detail, MyModel)

class Admin_test_contents(admin.ModelAdmin):
	list_display=('distro', 'pmid', 'title')
admin.site.register(Article, Admin_test_contents)


	
