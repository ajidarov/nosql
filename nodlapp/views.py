from django.db.models.aggregates import Count, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from .models import *
from .forms import *

# Create your views here.
class MultipleModelView(TemplateView):
    template_name = 'nodlapp/index.html'

    def get_context_data(self, **kwargs):
         context = super(MultipleModelView, self).get_context_data(**kwargs)
         context['subjects'] = Subject.objects.all()
         context['groups'] = Groups.objects.all()
         context['submissions'] = Submission.objects.all()
         context['weeks'] = Week.objects.all()
         return context

class SubjectDetailView(DetailView):
    model = Subject
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['sweeks'] = Week.objects.filter(subject=self.kwargs['pk'])
        context['weeks'] = Week.objects.all()
        context['submissions'] = Submission.objects.values('week').annotate(total=Count('id'))
        return context

class WeekDetailView(DetailView):
    model = Week
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['weeks'] = Week.objects.all()
        context['submissions'] = Submission.objects.filter(week=self.kwargs['pk']).order_by('-last_upload')
        return context


class CreateSubmissionView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'nodlapp/submission_form.html'
    def form_valid(self, form):
        form.instance.week = self.kwargs['pk']
        form.instance.student = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('nodl-home')


# class UpdateSubmissionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Submission
#     fields = ['file']

#     def form_valid(self, form):
#         form.instance.week = self.kwargs['pk']
#         form.instance.student = self.request.user
#         return super().form_valid(form)
    
#     def test_func(self):
#         sub = self.get_object()
#         if self.request.user == sub.student:
#             return True
#         return False