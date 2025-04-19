from django.shortcuts import render, redirect
from .models import StudyGroup
from .forms import StudyGroupForm

def studygroup_home(request):
    groups = StudyGroup.objects.all().order_by('-created_at')
    return render(request, 'study_groups/study_groups.html', {'groups': groups})

def create_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('study_groups:home')
    else:
        form = StudyGroupForm()
    return render(request, 'study_groups/create_group.html', {'form': form})
