from django.contrib import admin
from models import *

class user_results_1bb_admin(admin.ModelAdmin):
        list_display=('user', 'system', 'test_id','datetime', 'path' )
admin.site.register(user_results_1bb, user_results_1bb_admin)


class eval_meas_1bb_admin(admin.ModelAdmin):
        list_display=('system', 'testset' )
admin.site.register(evaluation_measures_1bb, eval_meas_1bb_admin)

