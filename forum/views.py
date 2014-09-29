# -*- coding: utf-8 -*-
import logging

from django.shortcuts import redirect, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from common.pagination import paginate

from forum.models import Category, Forum, Topic, Post
from forum.forms import PostForm, TopicForm, TopicDeleteForm


def get_post_form(request, topic):
    if request.user.is_authenticated():
        instance = Post(topic=topic, user=request.user)
        form = PostForm(request.POST or None, instance=instance)
        return form
    else:
        return None

@login_required
def home_page(request):
    cats = Category.objects.order_by('position')
    context = {'cats': cats,
            }
    return render(request, 'pybb/home_page.html', context)

@login_required
def forum_page(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    context = {'forum': forum,
            }
    return render(request, 'pybb/forum_page.html', context)


@login_required
def topic_page(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    posts = Post.objects.filter(topic=topic).order_by('created')
    post_form = get_post_form(request, topic)
    context = {'topic': topic,
               'posts': posts,
               'post_form': post_form,
            }
    return render(request, 'pybb/topic_page.html', context)


from django.core.mail import EmailMessage

@login_required
def post_add(request):
    topic_id = request.GET.get('topic')
    topic = get_object_or_404(Topic, pk=topic_id)
    form = get_post_form(request, topic)
    if form.is_valid():
        form.save()
	EmailMessage("[BioASQ]: New post in the platform", "There is a new post in the forum of the BioASQ Participants Area! \n It is in the topic '%s'" %topic, "admin@bioasq.org", to=["geompalik@hotmail.com", "akrithara@iit.demokritos.gr"]).send()
        return redirect(topic)
    context = {'form': form,
               'topic': topic,
            }
    return render(request, 'pybb/post_add.html', context)


@login_required
def topic_add(request):
    forum_id = request.GET.get('forum')
    forum = get_object_or_404(Forum, pk=forum_id)
    form = TopicForm(request.POST or None)
    if form.is_valid():
	EmailMessage("[BioASQ]: New post in the platform", "There is a new topic in the forum of the BioASQ Participants Area! \nIt is in the category '%s'" %forum, "admin@bioasq.org", to=["geompalik@hotmail.com", "akrithara@iit.demokritos.gr"]).send()
        topic = Topic.objects.create(
            name=form.cleaned_data['name'],
            forum=forum)
        post = Post.objects.create(
            topic=topic,
            user=request.user,
            content=form.cleaned_data['content'],
        )
        messages.success(request, u'Topic Created Successfully!')
        return redirect(topic)
    context = {'form': form,
               'forum': forum,
            }
    return render(request, 'pybb/topic_add.html', context)


@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if not request.user.is_superuser:
        messages.error(request, u'You have not permission to delete threads')
        return reverse('pybb:home_page')
    if request.method == 'POST':
        form = TopicDeleteForm(request.POST)
    else:
        form = TopicDeleteForm()
    if form.is_valid():
        topic.delete()
        messages.success(request, u'Topic Deleted')
        return redirect('pybb:home_page')
    context = {'topic': topic, 'form': form,
            }
    return render(request, 'pybb/topic_delete.html', context)
