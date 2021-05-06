from django.shortcuts import render
from django.http import HttpResponse
from login.models import User
from django.contrib import messages
from project.models import User_of_project,Project
from userStory.models import UserStory
import datetime
from login.views import getNowUser


def createPro(request):#מציג את כל הפרויקטים של המשתמש הנוכחי
    global nowUser
    nowUser=getNowUser()
    projectsUser=User_of_project.objects.filter(pk_user=nowUser.userName)
    projects=[]
    for pu in projectsUser:
        projects+=[(Project.objects.get(name=pu.pk_project))]
    global myProjects
    myProjects=projects
    
    return render(request,'projects/myProjects.html',{'projects':myProjects,'user':nowUser})

def buttonAddProject(request):#הכפתור שמפנה אותי לדף הוספת פרויקט
    users=list(user for user in User.objects.all() if not user.userName==nowUser.userName)
    return render(request,'projects/addProject.html',{'users':users})

def saveNewProject(request):
    #הכפתור שבתוך דף"הוספת פרויקט" מכניס לבסיס נתונים
    nameProject=request.POST.get('nameProject', None)
    users=request.POST.getlist('users', [])
    if Project.objects.filter(name=nameProject):
        messages.success(request, 'The project name is already in use')
        return buttonAddProject(request)
    else:
        project=Project(name=nameProject,teamLeader=nowUser.userName,date=datetime.datetime.now())
        project.save()
        users+=[nowUser.userName]

        for userName in users:
            userTemp=User.objects.get(userName=userName)
            ufp=User_of_project(pk_user=userTemp.userName,pk_project=project.name)
            ufp.save()
        projectsUser=User_of_project.objects.filter(pk_user=nowUser.userName)
        projects=[]
        for pu in projectsUser:
            projects+=[(Project.objects.get(name=pu.pk_project))]
        myProjects=projects
    return render(request,'projects/myProjects.html',{'projects':myProjects,'user':nowUser})


def deleteProject(request,nameProject):
    project = Project.objects.get(name=nameProject)
    project.delete()

    ufp=User_of_project.objects.filter(pk_project=nameProject)# למחוק קשרים בין משתמשים לפרויקט
    for x in ufp:
        x.delete()

    userSroeies=UserStory.objects.filter(nameProject=nameProject)#למחוק סיפורים שקשורים לפרויקט
    for x in userSroeies:
        x.delete()

    projectsUser=User_of_project.objects.filter(pk_user=nowUser.userName)
    projects=[]
    for pu in projectsUser:
        projects+=[(Project.objects.get(name=pu.pk_project))]
    myProjects=projects
    return render(request,'projects/myProjects.html',{'projects':myProjects,'user':nowUser})

def setNowUserProject(user):
    global nowUser
    nowUser=user