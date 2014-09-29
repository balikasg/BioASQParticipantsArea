from django.contrib import admin
from models import *

###################################################
class task1b_admin(admin.ModelAdmin):
	list_display=('test_id', 'phase',  'number_of_questions', 'number_of_downloads')
admin.site.register(Detail1b, task1b_admin)

class gold_question_admin(admin.ModelAdmin):
        list_display=('question_id', 'type', 'testset' )
admin.site.register(golden_question_1b, gold_question_admin)


class user_results_1b_admin(admin.ModelAdmin):
        list_display=('user', 'system', 'test_id','datatime', 'path' )
admin.site.register(user_results_1b, user_results_1b_admin)


class log_1b_admin(admin.ModelAdmin):
        list_display=('user', 'system', 'test_id', 'comment' )
admin.site.register(upload_information_for_1b, log_1b_admin)


class eval_1b_admin(admin.ModelAdmin):
        list_display=('user', 'testset' )
admin.site.register(evaluation_measures_1b, eval_1b_admin)


