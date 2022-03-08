from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        
       
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            # 'html': " ".join(self.html),
            # 'key': settings.HTML_HREF_REPLACE_KEY,
            # 'tag': self.group_tag
        }

        kwargs.update(context)
        return super(IndexView, self).get_context_data(**kwargs)


class IndexThemeView(LoginRequiredMixin,TemplateView):
    template_name = 'index/tpl/theme.html'

    def get(self, request, *args, **kwargs):
        
       
        return super(IndexThemeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            # 'html': " ".join(self.html),
            # 'key': settings.HTML_HREF_REPLACE_KEY,
            # 'tag': self.group_tag
        }

        kwargs.update(context)
        return super(IndexThemeView, self).get_context_data(**kwargs)

class IndexNoteView(LoginRequiredMixin,TemplateView):
    template_name = 'index/tpl/note.html'

    def get(self, request, *args, **kwargs):
        
       
        return super(IndexNoteView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            # 'html': " ".join(self.html),
            # 'key': settings.HTML_HREF_REPLACE_KEY,
            # 'tag': self.group_tag
        }

        kwargs.update(context)
        return super(IndexNoteView, self).get_context_data(**kwargs)

class IndexMessageView(LoginRequiredMixin,TemplateView):
    template_name = 'index/tpl/message.html'

    def get(self, request, *args, **kwargs):
        
       
        return super(IndexMessageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            # 'html': " ".join(self.html),
            # 'key': settings.HTML_HREF_REPLACE_KEY,
            # 'tag': self.group_tag
        }

        kwargs.update(context)
        return super(IndexMessageView, self).get_context_data(**kwargs)

class IndexAboutView(LoginRequiredMixin,TemplateView):
    template_name = 'index/about.html'

    def get(self, request, *args, **kwargs):
        
       
        return super(IndexAboutView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            # 'html': " ".join(self.html),
            # 'key': settings.HTML_HREF_REPLACE_KEY,
            # 'tag': self.group_tag
        }

        kwargs.update(context)
        return super(IndexAboutView, self).get_context_data(**kwargs)