from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudyGroup
from .forms import StudyGroupForm

@login_required
def home(request):
    groups = StudyGroup.objects.all()
    return render(request, 'study_groups/study_groups.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)  # Add creator as first member
            messages.success(request, 'Study group created successfully!')
            return redirect('study_groups:home')
    else:
        form = StudyGroupForm()
    return render(request, 'study_groups/create_group.html', {'form': form})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    
    if request.user in group.members.all():
        messages.warning(request, 'You are already a member of this group.')
    elif group.members.count() >= group.max_members:
        messages.error(request, 'This group is full.')
    else:
        group.members.add(request.user)
        messages.success(request, f'You have joined {group.name}!')
    
    return redirect('study_groups:home')
