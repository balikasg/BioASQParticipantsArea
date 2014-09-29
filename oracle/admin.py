from django.contrib import admin
from models import *

class eval_oracle_admin(admin.ModelAdmin):
        list_display=('user', 'test_id', 'timestamp')
admin.site.register(eval_meas_oracle, eval_oracle_admin)

class eval_oracle_1b_admin(admin.ModelAdmin):
        list_display=('user', 'test_id', 'timestamp')
admin.site.register(eval_meas_oracle_1b, eval_oracle_1b_admin)
	

class eval_oracle_1bb_admin(admin.ModelAdmin):
	list_display=('system', 'testset', 'timestamp', 'is_visible')
admin.site.register(eval_measi_oracle_1bb, eval_oracle_1bb_admin)



class log_admin(admin.ModelAdmin):
        list_display=('user', 'test_id', 'timestamp', 'comment')
admin.site.register(log_oracle, log_admin)
