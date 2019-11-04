from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from ser.models import Item,Post                                   ######for admin login
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from .forms import ExtendedUserCreationForm, UserProfileForm,Editprofile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import requests


def index(request):
    if request.user.groups.filter(name__in=['keeper']).exists():
        if request.user.is_authenticated:
            username = request.user.username
            email= request.user.email
            first_name= request.user.first_name

            current_user=request.user
            obj=UserProfile.objects.get(user=current_user)
            flat_number=obj.flat_number
            mobile_number=obj.mobile_number  
        else:
                username='not logged in'
                flat_number='unknown'
                email='unknown'
                mobile_number='unknown'
                first_name='unknown'


        context = {'username': username,'flat_number': flat_number,'mobile_number': mobile_number,'email':email,'first_name': first_name}

        return render(request, 'caretaker.html', context)


    else:

        if request.user.is_authenticated:
            username = request.user.username
            email= request.user.email
            first_name= request.user.first_name

            current_user=request.user
            obj=UserProfile.objects.get(user=current_user)
            flat_number=obj.flat_number
            mobile_number=obj.mobile_number

            
        else:
                username='not logged in'
                flat_number='unknown'
                email='unknown'
                mobile_number='unknown'
                first_name='unknown'

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4f3755118604d970d9bd420b4d9e1f11'
    city='Kochi'
    r = requests.get(url.format(city)).json()
    # print(r)
    city_weather = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
        'wind':r['wind']['speed'],
        
    }




    context = {'username': username,'flat_number': flat_number,'mobile_number': mobile_number,'email':email,'first_name': first_name,'city_weather':city_weather}

    return render(request, 'index.html', context)
@login_required
def deliver_item(request):

        order_list=Item.objects.all().order_by('-created')
        info=[]
        for x in order_list:
            y={'flnum':x.flat_number}
            info.append(y)
                                                        #pagination
        paginator=Paginator(info,5)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            info = paginator.page(page)
        except(EmptyPage, InvalidPage):
            info=paginator.page(paginator.num_pages)
                                                        #/pagination     
        context={
                'info':info
            }    
        return render(request,'shopkeeper.html',context)

@login_required
def deliver_service(request):

        order_list=Post.objects.all().order_by('-created')
        info=[]
        for x in order_list:
            y={'flnum':x.flat_number}
            info.append(y)
        paginator=Paginator(info,5)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            info = paginator.page(page)
        except(EmptyPage, InvalidPage):
            info=paginator.page(paginator.num_pages)
                                                        #/pagination     
        context={
                'info':info
            }    
        return render(request,'shopkeeper2.html',context)

class caretaker(LoginRequiredMixin,ListView):
    login_url = '/index/'
    
    model = Item
    template_name = 'received_orders.html'



    
    def get_queryset(self):

        category = self.kwargs.get('category')
        
        return Item.objects.filter(flat_number=category)



class caretaker2(LoginRequiredMixin,ListView):
    login_url = '/index/'
   
    model = Post
    template_name = 'received_orders2.html'
    
    def get_queryset(self):

        category = self.kwargs.get('category')
        # print (category)
        
        
        return Post.objects.filter(flat_number=category)





def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES or None)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')


    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()
    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'register.html', context)



@login_required
def edit(request):
    
    
    
    # if request.method == 'POST':
        
    #     form = Editprofile(request.POST,instance=request.user)
    #     form1=UserProfileForm(request.POST,instance=request.user)
    #     if form.is_valid()  and form1.is_valid():
    #         form1.save()
    #         form.save()
    #         print("valid")
    #         return redirect('index')
    # else:
      
    #     form = Editprofile(instance=request.user)
    #     form1 = UserProfileForm(instance=request.user)
    # return render(request, 'edit.html', {
    #     'form': form,'form1':form1
    # })


    if request.method == 'POST':
        form=Editprofile(request.POST)
        profile_form=UserProfileForm(request.POST)
        

        try:
            uname = request.POST['username']
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            email = request.POST['email']
            flat = request.POST['flat_number']
            mob = request.POST['mobile_number']
                                ####
            user = User.objects.get(username=request.user)
            profile = UserProfile.objects.get(user=user)
            user.username = uname
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
            profile.flat_number = flat
            profile.mobile_number = mob
            
            
            profile.save()
            
            return redirect('/profile')
        except:
            return render(request,'edit.html',{'form':form,'form1':profile_form,})
    else:
        user = User.objects.get(username=request.user)
        form = Editprofile(instance=user)
        profile = UserProfile.objects.get(user=user)
        profile_form = UserProfileForm(instance=profile)
        return render(request, 'edit.html', {
                'form': form, 'form1': profile_form,
            })



@login_required
def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        email= request.user.email
        first_name= request.user.first_name
        last_name= request.user.last_name

        current_user=request.user
        obj=UserProfile.objects.get(user=current_user)
        flat_number=obj.flat_number
        mobile_number=obj.mobile_number
        pic=obj.pro_pic

        
    else:
            username='not logged in'
            flat_number='unknown'
            email='unknown'
            mobile_number='unknown'
            first_name='unknown'
            last_name='unknown'
    


    context = {'username': username,'flat_number': flat_number,'mobile_number': mobile_number,'email':email,'first_name': first_name,'last_name': last_name, 'pic':pic }

    return render(request, 'pro.html', context)

