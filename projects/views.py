from .models import Project
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddProjectForm, AddTaskForm, AddDocumentForm

@login_required
def my_projects(request):
    projects = Project.objects.filter(supervisor=request.user).order_by('-created_at')
    if not projects:
        message = 'No projects found.'
        return render(request, 'projects/my_projects.html', {'message': message})
    return render(request, 'projects/my_projects.html', {'my_projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = AddProjectForm(request.POST, request.FILES, supervisor=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.supervisor = request.user  
            project.save()
            return redirect('my_projects')  
    else:
        form = AddProjectForm(supervisor=request.user)

    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def detele_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id, supervisor=request.user)
        if request.method == 'POST':
            project.delete()
            return redirect('my_projects')
        return render(request, 'projects/delete_project.html', {'project': project})
    except Project.DoesNotExist:
        return render(request, 'projects/my_projects.html', {'message': 'Project not found.'})
    
@login_required
def add_task(request, project_id):
    try:
        project = Project.objects.get(id=project_id, supervisor=request.user)
        if request.method == 'POST':
            form = AddTaskForm(request.POST, user=request.user)
            if form.is_valid():
                task = form.save(commit=False)
                task.project = project
                task.save()
                return redirect('my_projects')
        else:
            form = AddTaskForm(user=request.user)

        return render(request, 'projects/add_task.html', {'form': form, 'project': project})
    except Project.DoesNotExist:
        return render(request, 'projects/my_projects.html', {'message': 'Project not found.'})
    

@login_required
def add_document(request, project_id):
    try:
        project = Project.objects.get(id=project_id, supervisor=request.user)
        if request.method == 'POST':
            form = AddDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                document = form.save(commit=False)
                document.project = project
                document.save()
                return redirect('my_projects')
        else:
            form = AddDocumentForm()

        return render(request, 'projects/add_document.html', {'form': form, 'project': project})
    except Project.DoesNotExist:
        return render(request, 'projects/my_projects.html', {'message': 'Project not found.'})