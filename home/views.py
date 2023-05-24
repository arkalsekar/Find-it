from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from .models import Job, Profile
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string 
import uuid 
import random 
import time

# Create your views here.
def index(request):
    all_jobs = Job.objects.all()
    data = {"all_jobs": all_jobs}
    return render(request, 'index.html', context=data)

@login_required
def relevant(request):
    user_profile = get_object_or_404(Profile, username=request.user)
    all_jobs = Job.objects.all()
    
    # relevant_jobs = Job.objects.filter(title__icontains=user_profile.interested_jobs) or Job.objects.filter(job_description__icontains=user_profile.interested_jobs) or Job.objects.filter(tags__icontains=user_profile.techonologies) or  Job.objects.filter(tags__icontains=user_profile.interested_jobs)

    all_relevant_jobs_id = []

    for i in all_jobs:
        content_list = [user_profile.techonologies, i.job_description]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(content_list)
        matrix = cosine_similarity(count_matrix)
        result = (matrix[1][0]*100).round(2)
        print(result)

        if round(result) > 7:
            all_relevant_jobs_id.append(i.id)

    # print(all_relevant_jobs_id)
    
    relevant_jobs = Job.objects.filter(id__in=all_relevant_jobs_id)

    data = {'relevant_jobs': relevant_jobs}
    return render(request, 'relevant.html', data)

@login_required
def profile(request):

    if request.method == "POST":
        username = request.user
        first_name = username.first_name
        last_name = username.last_name
        jobsinterested = request.POST['jobsinterested']
        bio = request.POST['bio']
        technologies = request.POST['technologies']
        profile = Profile(username=username, first_name=first_name, last_name=last_name, interested_jobs=jobsinterested, bio=bio, techonologies=technologies)
        profile.save()
        messages.success(request, "User Profile Saved Successfully")
    
        
    return render(request, 'profile.html')


# Create your views here.
def signup(request):
    if request.method=='POST':
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['signupemail']
        password = request.POST['signuppassword1']
        password2 = request.POST['signuppassword2']
    
        # Checks for creating User
        if len(uname) < 3:
            messages.error(request, 'Username should be greater then 3')

        create_newuser = User.objects.create_user(uname, email, password2)
        create_newuser.first_name = fname
        create_newuser.last_name = lname
        create_newuser.save()
    
        messages.success(request, f'User {uname} created successfully, Go ahead and Login to your Account')

    return redirect('/')


def handle_login(request):
    if request.method=='POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']    

        user = authenticate(request, username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, f'Successfully Logged in as - {user}')
            return redirect('profile')
        else:
            messages.error(request, 'No Such User exists')
            return redirect('/')
    else:
        messages.error(request, f'{user} Details dont Match the Database Please Try Agians')
        return redirect('/')


@login_required
def handle_logout(request):
    if not request.user.is_authenticated:
        return redirect('/')
    logout(request)
    messages.success(request, f' Successfully Logged Out')
    return redirect('/')

