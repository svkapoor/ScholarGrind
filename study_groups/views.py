from django.shortcuts import render

def studygroup_home(request):
    return render(request, 'study_groups/study_groups.html')