from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Task, Category
from .forms import TaskForm
from django.urls import reverse
from django.shortcuts import render,redirect





class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = '/tasks/'
    def create_task(request):
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('task_list'))
            else:
                form = TaskForm()
                return render(request, 'task_form.html', {'form': form})