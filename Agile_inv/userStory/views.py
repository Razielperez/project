from django.shortcuts import render
from userStory.models import UserStory
from login.models import User
from project.models import User_of_project,Project
from project.views import getNowUser,createPro

def returnHomeProject(request):
    userName=getNowUser()
    return createPro(request)
def userStoryPage(request,nameProject):
    my_stories = UserStory.objects.filter(nameProject=nameProject)
    global project
    project=Project.objects.get(name=nameProject)
    userOfProject=User_of_project.objects.filter(pk_project=nameProject) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)}) 

def insertStory(request):
    
    ufp = User_of_project.objects.filter(pk_project=project.name)
    my_users=[]
    for x in ufp:
        my_users+=[User.objects.get(userName=x.pk_user)]
    return render(request,'createStory/createStory.html',{'users':(my_users),'range':(range(1,6))}) 


def submit_story(request):
    AssignTo = request.POST.get('Assign', None)
    Priority = request.POST.get('Priority', None) 
    Content = request.POST.get('Content', None) 
    story = UserStory(nameProject=project.name,content=Content,priority=Priority,assign=AssignTo)
    story.save()
    my_stories =UserStory.objects.filter(nameProject=project.name)
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)})

def delete_story(request,id):
    obj = UserStory.objects.get(id=id)
    obj.delete()
    my_stories =UserStory.objects.filter(nameProject=project.name) 
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)}) 
    

def updateToDone(request,id):
    obj = UserStory.objects.get(id=id)
    obj.status = "Done"
    obj.save()
    my_stories = UserStory.objects.filter(nameProject=project.name)
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)})



def allStories(request):
    my_stories = UserStory.objects.filter(nameProject=project.name)
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)}) 


def FilterNotDone(request):
    objects = UserStory.objects.filter(nameProject=project.name)
    container = []
    for o in objects:
        if o.status == "Not Done":
            container+=[o]
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(container),'project':(project),'userOfProject':(userOfProject)}) 

def filterMyUserStory(request):
    user=getNowUser()
    my_stories = UserStory.objects.filter(nameProject=project.name).filter(assign=user.userName)
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)})

def updateUserStory(request,id):
    user_story =  UserStory.objects.get(id=id)
    ufp = User_of_project.objects.filter(pk_project=project.name)
    my_users=[]
    for x in ufp:
        my_users+=[User.objects.get(userName=x.pk_user)]
    return render(request,'createStory/createStory.html',{'user_story':(user_story),'users':(my_users),'range':(range(1,6))}) 

def updateAction(request,id):
    user_story =  UserStory.objects.get(id=id)
    user_story.assign = request.POST.get('Assign', None)
    user_story.priority= request.POST.get('Priority', None) 
    user_story.content = request.POST.get('Content', None) 
    user_story.save()    
    my_stories =UserStory.objects.filter(nameProject=project.name)
    userOfProject=User_of_project.objects.filter(pk_project=project.name) 
    return render(request,'storiesView/storiesView.html',{'stories':(my_stories),'project':(project),'userOfProject':(userOfProject)})
    
def testF(request):
    xx=UserStory.objects.all()
    for x in xx:
        x.delete()

    xx=Project.objects.all()
    for x in xx:
        x.delete()
    
    xx=User_of_project.objects.all()
    for x in xx:
        x.delete()
    
    
    return render(request,'storiesView/test.html',{})
    
    
    