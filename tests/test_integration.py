from django.test import TestCase, Client
from django.urls import reverse
from project.models import Project, User_of_project
from project.views import setNowUserProject
from userStory.models import UserStory
from login.models import User
import json


class TestIntegration (TestCase):

    def setUp(self):
        self.client=Client()
        self.user = User.objects.create(
            firstName="Ploni",
            lastName="Almoni",
            userName="ploni123",
            password="123",
            role="teamLeader"
        )
        self.user2 = User.objects.create(
            firstName="Plonii",
            lastName="Almonii",
            userName="ploni1234",
            password="123",
            role="teamLeader"
        )
        self.project1 = Project.objects.create(
            name="project1",
            teamLeader=self.user.userName,
            date="2021-05-05"
        )
        self.project2 = Project.objects.create(
            name="project2",
            teamLeader=self.user2.userName,
            date="2021-05-05"
        )
        self.UOP1 = User_of_project.objects.create(
            pk_user=self.user.userName,
            pk_project=self.project1.name
        )
        self.user_story1 = UserStory.objects.create(
            nameProject=self.project1.name,
            content='Test_content',
            priority='1',
            assign=self.user.userName,
            status='Not Done'
        ) 
        self.user_story2 = UserStory.objects.create(
            nameProject=self.project2.name,
            content='Test_content2',
            priority='2',
            assign=self.user2.userName,
            status='Not Done'
        )
        setNowUserProject(self.user)
        self.createPro_url=reverse('project:createPro')
        self.deleteProject1_url=reverse('project:deleteProject',args=[self.project1.name])
        self.createProject_url=reverse('project:saveNewProject')
        
    def test_deleteProject_POST_can_delete(self):
        response = self.client.post(self.deleteProject1_url,{
            'nameProject': self.project1.name
        })
        self.assertNotContains(response,self.project1)
        self.assertFalse(Project.objects.filter(name=self.project1.name))
        self.assertTemplateUsed(response, 'projects/myProjects.html')
    
    def test_deleteUserStory_POST_can_delete(self):
        response = self.client.post(self.deleteProject1_url,{
            'nameProject': self.project1.name
        })
        self.assertNotContains(response,self.user_story1)
        self.assertFalse(UserStory.objects.filter(id=self.user_story1.id))

    def test_createProject2_POST_can_create(self):
        newName="testCreateProjectName"
        response = self.client.post(self.createProject_url,
        {'nameProject': newName,
        'users':[self.user2.userName]} )

        self.assertTrue(Project.objects.filter(name=newName))
        self.assertNotContains(response,self.user_story2)
        self.assertNotContains(response,self.project2)
        self.assertTemplateUsed(response, 'projects/myProjects.html')
