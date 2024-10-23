from django.shortcuts import render,redirect

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
        Profile_Pic=request.FILES.get("Profile_Pic")
        contact_no=request.POST.get("contact_no")
    
        
        if password==Confirm_password:
            
            
            user=customUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                Profile_Pic=Profile_Pic,
                contact_no=contact_no,
            )
            if user_type=='seeker':
                seekerProfileModel.objects.create(user=user)
                
            elif user_type=='recruiter':
                recruiterProfileModel.objects.create(user=user)
            
            return redirect("signInPage")
            
    return render(request,"signupPage.html")


def signInPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return redirect('homePage') 
            else:
                return redirect('signInPage')

        except customUser.DoesNotExist:
            return redirect('signInPage')

    return render(request, 'signInPage.html')

@login_required
def homePage(request):
    
    
    return render(request,"homePage.html")


def logoutPage(request):
    
    logout(request)
    
    return redirect('signInPage')

@login_required
def profilePage(request):
    
    return render(request,"profilePage.html")

def addJobPage(request):

    current_user=request.user
    if current_user.user_type == "recruiter":
        if request.method=="POST":
            jobs=JobModel()
            jobs.user=current_user
            jobs.job_title=request.POST.get("job_title")
            jobs.vacancy=request.POST.get("vacancy")
            jobs.skills=request.POST.get("skills")
            jobs.category=request.POST.get("category")
            jobs.description=request.POST.get("description")
            jobs.job_Pic=request.FILES.get("job_Pic")
            
            jobs.save()
           
            return redirect("jobFeed")
    
    return render(request,"addJobPage.html")

def createdJobPage(request):

    current_user=request.user
    jobs=JobModel.objects.filter()

    context= {
        'jobs': jobs
    }
    
    return render(request,"createdJobPage.html",context)

def jobFeed(request):

    current_user=request.user
    jobs=JobModel.objects.all()

    context= {
        'jobs': jobs
    }
    
    return render(request,"jobFeed.html",context)

def deleteJob(request,job_id):

    jobs=JobModel.objects.filter(id=job_id)
    jobs.delete()

    
    return redirect("createdJobPage")


def viewJOb(request,job_id):

    jobs=JobModel.objects.filter(id=job_id)

    context= {
        'jobs': jobs
    }
    
    
    return render(request,"viewJOb.html",context)

def editJob(request,job_id):

    jobs=JobModel.objects.get(id=job_id)

    context= {
        'jobs': jobs
    }

    current_user=request.user
    if current_user.user_type == "recruiter":
        if request.method=="POST":
            jobs=JobModel()
            jobs.id=request.POST.get("job_id")
            jobs.user=current_user
            jobs.job_title=request.POST.get("job_title")
            jobs.vacancy=request.POST.get("vacancy")
            jobs.skills=request.POST.get("skills")
            jobs.category=request.POST.get("category")
            jobs.description=request.POST.get("description")
            jobs.job_Pic=request.FILES.get("job_Pic")
            
            jobs.save()
           
            return redirect("createdJobPage")
    

    return render(request,"editJob.html",context)



