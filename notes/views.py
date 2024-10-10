from django.shortcuts import render,redirect
from django.views.generic import View
from notes.forms import TaskForm,RegisterForm,SignInForm
from notes.models import Task
from django.contrib import messages
from django import forms
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from notes.decorators import signin_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.
decs=[signin_required,never_cache]
@method_decorator(decs,name='dispatch')
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form_instance=TaskForm()
        return render(request,'taskcreate.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=TaskForm(request.POST)
        if form_instance.is_valid():
            form_instance.instance.user=request.user
            form_instance.save()
            messages.success(request,'task created')
            return redirect('task-list')
        else:
            messages.error(request,'failed to add')
            return render(request,'taskcreate.html',{'form':form_instance})
@method_decorator(decs,name='dispatch')
class TaskListView(View):
    def get(self,request,*args,**kwargs):

       
        search_text=request.GET.get('search_text')
        selected_category=request.GET.get("category","all")
        if selected_category == 'all':
            # qs=Task.objects.all()
            qs=Task.objects.filter(user=request.user)
        else:
            # to filter by logged in user tasks
            qs=Task.objects.filter(category=selected_category,user=request.user)
        if search_text!=None:
            qs=Task.objects.filter(user=request.user)
            qs=qs.filter(Q(title__icontains=search_text)|Q(description__icontains=search_text))
           
        return render(request,'tasklist.html',{'tasks':qs,"selected":selected_category})
    
       
@method_decorator(decs,name='dispatch')
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        return render(request,'taskdetail.html',{'task':qs})

@method_decorator(decs,name='dispatch')
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):
        #extract pk from kwargs

        id=kwargs.get("pk")
        # fetch task object with id
        task_obj=Task.objects.get(id=id)

        # initialize task with task object only if form is ModelForm use instance
        form_instance=TaskForm(instance=task_obj)

        #add status field in form_instance
        form_instance.fields['status']=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={'class':'form-control form-select'}),initial=task_obj.status)

        return render(request,'taskedit.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        # extract id from kwargs
        id=kwargs.get('pk')

        task_obj=Task.objects.get(id=id)


        # declare form instance with request.post
        form_instance=TaskForm(request.POST,instance=task_obj)
        
        # check errors
        if form_instance.is_valid():
            # add status to form instance
            form_instance.instance.status=request.POST.get('status')
            form_instance.save()
            messages.success(request,'updated!')
            return redirect('task-list')
        else:
            messages.error(request,'failed to update')
            return render(request,'taskedit.html',{'form':form_instance})

           
@method_decorator(decs,name='dispatch')
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        # extract id and delete task object with id
        Task.objects.get(id=kwargs.get('pk')).delete()
        return redirect('task-list')

@method_decorator(decs,name='dispatch')
class TaskSummaryView(View):
    def get(self,request,*args,**kwargs):

        # qs=Task.objects.all()
        qs=Task.objects.filter(user=request.user)
        total_task_count=qs.count()
        category_summary=qs.values("category").annotate(cat_count=Count("category"))
        # print(category_summary)
        status_summary=qs.values("status").annotate(status_count=Count("status"))
        # print(status_summary)
        context={
            "total_task_count":total_task_count,
            "category_summary":category_summary,
            "status_summary":status_summary
        }
        return render(request,"dashboard.html",context)

class SignUpView(View):
    template_name='register.html'
    def get(self,request,*args,**kwargs):
        form_instance=RegisterForm()
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=RegisterForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            User.objects.create_user(**data)
            return redirect('signin')
        else:
            return render(request,self.template_name,{'form':form_instance})
            
class SignInView(View):
    template_name='login.html'
    def get(self,request,*args,**kwargs):
        form_instance=SignInForm()
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)
        # if form is valid
        if form_instance.is_valid():
            uname=form_instance.cleaned_data.get('username')
            pwd=form_instance.cleaned_data.get('password')

            # authenticate
            user_obj=authenticate(request,username=uname,password=pwd)
            # if user object is valid then call login to start session
            if user_obj:
                login(request,user_obj)
                return redirect('task-list')
        return render(request,self.template_name,{'form':form_instance})

@method_decorator(decs,name='dispatch')
class SignOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')

class DashboardView(View):
    template_name='dashboard.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)


            