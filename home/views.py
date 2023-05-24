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
def search(request):
    query = request.GET['query']
    
    if len(query) < 1:
        query = "Python Developer "

    relatedJobs = Job.objects.filter(title__icontains=query) or Job.objects.filter(company_name__icontains=query) or Job.objects.filter(job_description__icontains=query) or Job.objects.filter(tags__icontains=query)
    
    params = {'relatedJobs': relatedJobs}
    return render(request, 'search.html', params)


@login_required
def relevant(request):
    user_profile = get_object_or_404(Profile, username=request.user)
    all_jobs = Job.objects.all()
    
    # relevant_jobs = Job.objects.filter(title__icontains=user_profile.interested_jobs) or Job.objects.filter(job_description__icontains=user_profile.interested_jobs) or Job.objects.filter(tags__icontains=user_profile.techonologies) or  Job.objects.filter(tags__icontains=user_profile.interested_jobs)

    all_relevant_jobs_id = []

    if user_profile.techonologies == None or user_profile.interested_jobs == None:
        data = {'relevant_jobs': [] }
        return render(request, 'relevant.html', data)
    
    elif len(user_profile.techonologies) < 1 or len(user_profile.interested_jobs)  < 1:
        data = {'relevant_jobs': [] }
        return render(request, 'relevant.html', data)

    for i in all_jobs:
        cv = CountVectorizer()

        content_list_1 = [user_profile.techonologies, i.job_description]
        count_matrix_1 = cv.fit_transform(content_list_1)
        matrix_1 = cosine_similarity(count_matrix_1)
        result_1 = (matrix_1[1][0]*100).round(2)
        
        content_list_2 = [user_profile.techonologies, i.tags]
        count_matrix_2 = cv.fit_transform(content_list_2)
        matrix_2 = cosine_similarity(count_matrix_2)
        result_2 = (matrix_2[1][0]*100).round(2)
                
        content_list_3 = [user_profile.interested_jobs, i.title]
        count_matrix_3 = cv.fit_transform(content_list_3)
        matrix_3 = cosine_similarity(count_matrix_3)
        result_3 = (matrix_3[1][0]*100).round(2)
        
        content_list_4 = [user_profile.bio, i.job_description]
        count_matrix_4 = cv.fit_transform(content_list_4)
        matrix_4 = cosine_similarity(count_matrix_4)
        result_4 = (matrix_4[1][0]*100).round(2)
        
        content_list_5 = [user_profile.interested_jobs, i.tags]
        count_matrix_5 = cv.fit_transform(content_list_5)
        matrix_5 = cosine_similarity(count_matrix_5)
        result_5 = (matrix_5[1][0]*100).round(2)
        

        if round(result_1) > 7 or round(result_2) > 7 or round(result_3) > 7 or round(result_4) > 7 or round(result_5) > 7:
            all_relevant_jobs_id.append(i.id)

    # print(all_relevant_jobs_id)
    
    relevant_jobs = Job.objects.filter(id__in=all_relevant_jobs_id)

    data = {'relevant_jobs': relevant_jobs}
    return render(request, 'relevant.html', data)

@login_required
def profile(request):
    current_user = Profile.objects.filter(username=request.user)
    
    if len(current_user) != 0:
        params = {'current_user': current_user}
        
        if request.method == "POST":
            updating_profile = Profile.objects.get(username=request.user)
            # print(updating_profile.first_name)

            updating_profile.username = request.user
            updating_profile.first_name = request.POST['fname']
            updating_profile.last_name = request.POST['lname']
            updating_profile.interested_jobs = request.POST['jobsinterested']
            updating_profile.bio = request.POST['bio']
            updating_profile.techonologies = request.POST['technologies']
            # profile = Profile(username=username, first_name=first_name, last_name=last_name, interested_jobs=jobsinterested, bio=bio, techonologies=technologies)
            updating_profile.save()
            messages.success(request, "User Profile Updated Successfully")
    
    else:
        params = {'current_user': ["", "", "", "", "", ""]}   

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
    
        
    return render(request, 'profile.html', params)


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

        user_profile = Profile(username=create_newuser, first_name=create_newuser.first_name, last_name=create_newuser.last_name, interested_jobs=" ", bio=" ", techonologies=" ")
        user_profile.save()

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

