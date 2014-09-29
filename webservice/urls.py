from django.conf.urls import patterns, url

urlpatterns = patterns('snippets.views',
	url(r'^tests/$', 'test_list'),
	url(r'^tests/(?P<pk>[0-9]+)/$', 'test_down'),
)
