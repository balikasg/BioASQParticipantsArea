# coding: utf-8
from django import forms

from forum.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class TopicForm(forms.Form):
    name = forms.CharField(label=u'Topic')
    content = forms.CharField(label=u'Post', widget=forms.Textarea)


class TopicDeleteForm(forms.Form):
    pass
