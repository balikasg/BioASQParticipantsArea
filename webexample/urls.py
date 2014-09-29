from django.conf.urls import*
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from views import*
from django.conf import settings
from registration.views import register
import regbackend
from webservice import views
from django.conf.urls import include
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
from django.contrib.admin.views.decorators import staff_member_required
from task1b.views import *
from task1bb.views import *
from oracle.views import *


urlpatterns = patterns('',
    url(r'^delete/$', deleter),
    url(r'^oracle/jsonGen/$', filterer),
    url(r'^accounts/register/$', register, {'backend': 'registration.backends.default.DefaultBackend','form_class': UserRegForm}, name='registration_register'),
    #url(r'login/$', login_user),
    #(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^home2/$', direct_to_template, { 'template': 'index2.html' }, 'index2' ),
    url(r'^profile/$', profile_edit),
    url(r'sendMessage/$', sendMessageToList),
    url(r'changeEmail/$', email_change),
    url(r'^tools/BioASQword2vec/$', word2vec),
    url(r'^info/BioASQword2vec/$', word2vecRead),
    #url('rouge/$', run_rouge),
    url(r'MeSH2013/$', download_mesh2013),
    url('add_system/$', add_a_new_system),
    url(r'changetasks/$', task_selection_edit),
    #url(r'/done/$', email_changed),
    url(r'CreateTest/$', create_tests),
    url(r'd3_4/$', d34),
    url(r'Tasks/b/eval_meas/$', d41),
    url(r'^vectorized_training_set/$', download_vect),
    url(r'^oracle/$', oracle),
    url(r'^oracle/makeGoldenDatabase/$', makeGoldenDatabase),    
    url(r'^raw_training_set/$', download_raw),
    url(r'^journalsTraining/$', journalsTraining),
    url(r'^cluster/$', cluster),
    url(r'^download/sampleData/task1a/$', sampleData1a),
    url(r'^download/sampleData/task1b/$', sampleData1b),
    url(r'^Tasks/$',direct_to_template, { 'template': 'Tasks.html' }, 'Tasks'),
    url(r'^Tasks/2a/trainingDataset/lucene/allMeSH/$', download_vect2014),
    url(r'^Tasks/2a/trainingDataset/lucene/selectionJournals/$', download_vect2014Limit),
    url(r'^Tasks/2a/trainingDataset/raw/allMeSH/$', download_raw2014),
    url(r'^Tasks/2a/trainingDataset/raw/selectionJournals/$', download_raw2014Limit),
    url(r'^Tasks/2a/MeSH/parentChild/$', meshMappingPC2014),
    url(r'^Tasks/2a/MeSH/mapping/$', meshMapping2014),
    url(r'^Tasks/A/getData/$', taskAData),
    url(r'^Tasks/1a/$', task1a),
    url(r'^Tasks/2a/$', task2a),
    url(r'^Tasks/2b/trainingDataset/$', training2b),
    url(r'^Tasks/2b/$', task1ba),
    url(r'^mapping/$', meshMapping),
    url(r'^pc-mapping/$', meshMapping2),
    url(r'^eval/$', evaluate),
    url(r'^eval/1b/phaseA/$', evaluate_1b),
    url(r'^eval/1bb/$', evaluate1bb),
    url(r'^tools/$', tools),
    url(r'^results/2a/$', results2a),
    url(r'^results/1b/phaseA/$', results1b),	
    url(r'^results/2b/phaseA/$', results2b),
    url(r'^results/1b/phaseB/$', results1bb),
    url(r'^results/2b/phaseB/$', results2bb),
    url(r'^results/b/phaseA/$', resultsOracleTaskA),
    url(r'^results/b/phaseB/$', resultsOracleTaskB),
    url(r'^oracle/results/task1a/$', resultsOracle),
    url(r'^results/$', results),
    url(r'^results/additional_testset_1a/$', results_additional_1a),
    url(r'^journals/$',journals),
    url(r'^Tasks/2a/results/(\d+)/([^/]+)/$', download_results),
    url(r'^Tasks/1b/phaseA/results/(\d+)/([^/]+)/$', download_results_1b),
    url(r'^Tasks/1b/phaseB/results/(\d+)/([^/]+)/$', download_results_1bb),
    url(r'^Tasks/b/resources/$', download_resources),
    url(r'^Tasks/2b/phaseA/(\d+)/$', download_test1ba),
    url(r'^Tasks/2b/phaseB/(\d+)/$', download_test1bb),
    url(r'^Tasks/1b/phaseA/dryRun/$', task1b_dry),
    url(r'^Tasks/1b/phaseB/dryRun/$', task1bb_dry),
    url(r'^Tasks/2b/phaseA/api/(\d+)/$', Task1baRemote),
    url(r'^Tasks/2b/phaseB/api/(\d+)/$', Task1bbRemote),
    url(r'^Tasks/2b/phaseA/$',task1ba),
    url(r'^Tasks/2b/phaseB/$',Task1bPhaseBSubmitWebInterface),
    url(r'^Tasks/2b/phaseA/submit/(\d+)/$', Task1bPhaseASubmitAPI),
    url(r'^Tasks/2b/phaseB/submit/(\d+)/$', Task1bPhaseBSubmitApi),
    url(r'^Tasks/1b/api/documentation/$', api_documentation),
    #url(r'^Tasks/2a/(\d+)/$', download_test),                            
    url(r'^data/raw/(\d+)/$', download_test),
    #url(r'^Tasks/2a/vectorized/(\d+)/$', download_vect_test),           
    url(r'^data/vectorized/(\d+)/$', download_vect_test),
    url(r'^contact/thankyou/', direct_to_template, { 'template': 'thanks.html' }, 'thanks'),
    url(r'^contact/', contactview),
    url(r'^general_information/$', direct_to_template, { 'template': 'general_information.html' }, 'genaral_Information'),
    url(r'^general_information/general_information_registration/$', direct_to_template, { 'template': 'general_information_registration.html' }, 'genaral_Information_registration'),
    url(r'^general_information/Task2a/$', direct_to_template, { 'template': 'general_information1a.html' }, 'genaral_Information1a'),
    url(r'^general_information/Task2b/$', direct_to_template, { 'template': 'general_information1b.html' }, 'task1b'),
    url(r'^faq/$', direct_to_template, { 'template': 'faq.html' }, 'faq'),

    url(r'^admin/', include(admin.site.urls)),
    #(r'^admin/(.*)', admin.site.urls),
	(r'^accounts/', include('registration.urls')),
	(r'^$', direct_to_template,
	        { 'template': 'index.html' }, 'index'),
)



#urlpatterns += staticfiles_urlpatterns()


urlpatterns +=patterns('forum.views',
    url(r'^forum/$', 'home_page', name='home_page'),
    url(r'^forum/(\d+)/$', 'forum_page', name='forum_page'),
    url(r'^topic/(\d+)/$', 'topic_page', name='topic_page'),
    url(r'^post/add/$', 'post_add', name='post_add'),
    url(r'^topic/add/$', 'topic_add', name='topic_add'),
    url(r'^topic/(\d+)/delete/$', 'topic_delete', name='topic_delete'),
)
urlpatterns +=patterns('',
	url(r'^tests/$', views.test_list.as_view()),
	url(r'^tests/(?P<pk>[0-9]+)/$', views.article_list.as_view()),
	url(r'^tests/uploadResults/(?P<pk>[0-9]+)/$', views.results1),
	url(r'^api-auth/', include('registration.urls',
                               namespace='rest_framework')),
)








#urlpatterns+=patterns('uploads.views',
#    url(r'^list/$', 'list', name='list'),
#)

#urlpatterns+=patterns('',
#    url(r'^captcha/', include('captcha.urls')),
#)


