from django.http import HttpResponse , JsonResponse
from django.shortcuts import render ,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile , RequestFriend
from main.models import Post , Comment , Share
from django.views.decorators.csrf import csrf_protect
import json
from django.core import serializers
from django.contrib  import messages
# Create your views here.


def signup_request(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render (request,'accounts/signup.html', {'error':'Sorry, Username is already exists'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('firstname'),
                    last_name=request.POST.get('lastname'),
                    email=request.POST.get('email'),
                    password=request.POST.get('password1'),
                    )
                auth.login(request,user)
                print(user ,"<-------------------create an account and login successfully")
                return redirect('index')
        else:
            return render (request,'accounts/signup.html', {'error':'Sorry, Password does not match'})
    else:
        return render(request,'accounts/signup.html')


def login_request(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            print(user , "<-------------------login successfully")
            return redirect('index')         
        else:
            return render (request,'accounts/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request, 'accounts/login.html')

@login_required
def logout_request(request):
    print(request.user , "<-------------------logout successfully")
    auth.logout(request)
    return redirect('login')


@login_required
def show_settings(request):
    mobile = Profile.objects.get(user=request.user).mobile
    photo = Profile.objects.get(user=request.user).photo
    return render(request , 'accounts/settings.html',context={'mobile':mobile,'profile_img':photo})

def profile(request,slug ):
    profile_obj = Profile.objects.get(slug=slug)
    posts = Post.objects.filter(user=profile_obj.user)
    number_of_posts = posts.count()
    request_exist = RequestFriend.objects.filter(send_from = request.user , send_to = profile_obj.user).exists() | RequestFriend.objects.filter(send_from = profile_obj.user , send_to = request.user).exists()
    comments = Comment.objects.all()
    my_share = Share.objects.filter(user = profile_obj.user)

    context={
        'posts': posts,
        'comments':comments,
        'shares':my_share,
        'count': number_of_posts,
        'friends':profile_obj.friends.all(),
        'number_of_friends':profile_obj.friends.all().count(),
        'user': profile_obj.user,
        'fullname': profile_obj.user.get_full_name(),

        'bio': profile_obj.bio,
        'img': profile_obj.photo,
        'country':profile_obj.country,
        'phone': profile_obj.mobile,
        'gender':profile_obj.gender,
        'joined': profile_obj.created_at,
        'request_exist':request_exist,
    }
    return render(request,'accounts/profile.html',context)


@csrf_protect
def add_friend(request):
    id = int(request.GET.get('userID')) # user that i send request for u
    user = User.objects.get(id = id)
    sender = request.user
    if not RequestFriend.objects.filter(send_from = sender , send_to = user).exists():
        obj = RequestFriend.objects.create(send_from = sender , send_to = user)
        obj.save()
        return HttpResponse("Request has been successfully")
    else:
        return HttpResponse("You already send Request before")

@csrf_protect
def delete_friend(request):
    id = int(request.GET.get('userID')) # user that i will delete from friends
    friend = User.objects.get(id = id)
    user = User.objects.get(id=request.user.id)
    my_profile = Profile.objects.get(user = user)
    profile_friend = Profile.objects.get(user = friend)
    if friend in my_profile.friends.all() and user in profile_friend.friends.all():
        my_profile.friends.remove(friend)
        my_profile.save()

        profile_friend.friends.remove(user)
        profile_friend.save()
        return HttpResponse("friend deleted successfully")
    return HttpResponse("User not Found")

def requestfriend(request):
    requestid = int(request.GET.get('requestid'))
    RequestFriend.objects.get(id=requestid).delete() 
    action = json.loads(request.GET.get('action'))

    if action == "confirm":#accept request
        id = int(request.GET.get('id'))#id of sender
        sender = User.objects.get(id=id)
        myprofile = Profile.objects.get(user=request.user)
        if sender not in myprofile.friends.all():
            friend = User.objects.get(id=id)
            myprofile.friends.add(friend)
            myprofile.save()
        sender_friends = sender.profile.friends.add(request.user)
        sender_friends.save()
    count = RequestFriend.objects.filter(send_to=request.user).count()
    return JsonResponse({"count":f'{count}'})

@csrf_protect
def search_friends(request):
    search = json.loads(request.POST.get('search'))
    if search:
        friends = Profile.objects.filter(slug__contains=search) | Profile.objects.filter(mobile__exact=search)
        people = serializers.serialize('json', friends )
        data ={'people':people}
        return JsonResponse(data)
    else:
        return HttpResponse(" search not found ")
    

def change_pass(request):
    old_pass = request.POST.get('old')
    new_pass = request.POST.get('new1')
    new_pass_confirm = request.POST.get('new2')
    print(old_pass , new_pass , new_pass_confirm)
    if new_pass == new_pass_confirm:
        user = User.objects.get(pk=request.user.id)
        if user.check_password(old_pass):
            user.set_password(new_pass)
            user.save()
            print("updated")
            logout_request(request)
        error = "Please enter correct old password again"
        return render(request,'accounts/settings.html',context={'error':error})
    error = "Please enter the same password for new password and confirmation"
    return render(request,'accounts/settings.html',context={'error':error})
        