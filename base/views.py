from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import login

##Usuario creado para pruebas del proyecto
##Username : jhon password: joh#12371

## MIN 1:21:03

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    #fields = '__all__' este campo no hace falta. La clase LoginView renderiza un formulario con los campos username y pasword por defecto
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'   
    template_name = 'base/task.html'
      
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')  

## Cambiar el nombre de la clase a TaskDelete para que el nombre sea consistente en el resto de las clases
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks') 

        