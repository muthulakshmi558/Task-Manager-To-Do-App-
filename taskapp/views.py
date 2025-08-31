from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from .models import Task
from .forms import TaskForm, DateFilterForm, RegisterForm

# Registration
def register_view(request):
    if request.user.is_authenticated:
        return redirect('task-list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('task-list')
    else:
        form = RegisterForm()
    return render(request, 'taskapp/register.html', {'form': form})

# Login
from django.contrib.auth.forms import AuthenticationForm
def login_view(request):
    if request.user.is_authenticated:
        return redirect('task-list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('task-list')
    else:
        form = AuthenticationForm()
    return render(request, 'taskapp/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'taskapp/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).order_by('due_date')
        # Date filter
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')
        if start:
            queryset = queryset.filter(due_date__gte=start)
        if end:
            queryset = queryset.filter(due_date__lte=end)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = DateFilterForm(self.request.GET)
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'taskapp/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'taskapp/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'taskapp/task_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'taskapp/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully!")
        return super().delete(request, *args, **kwargs)
