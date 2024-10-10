"""
URL configuration for TaskPro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notes import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/add/',views.TaskCreateView.as_view(),name='task-create'),
    path('tasks/all/',views.TaskListView.as_view(),name='task-list'),
    path('tasks/<int:pk>/change/',views.TaskUpdateView.as_view(),name='task-update'),
    path('tasks/<int:pk>/remove/',views.TaskDeleteView.as_view(),name='task-delete'),
    path("",views.TaskSummaryView.as_view(),name='task-summary'),
    path('register/',views.SignUpView.as_view(),name='signup'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    path('signout/',views.SignOutView.as_view(),name='signout'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
]
