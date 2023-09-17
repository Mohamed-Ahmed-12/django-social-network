from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Post , Comment 
from .forms import PostForm
from django.contrib.auth.models import User
from accounts.models import RequestFriend
'''
{{ request.user.get_full_name }} to display first name and last name
'''
@login_required(redirect_field_name='redirect',login_url='login')
def mainPage(request):
    #FORM TO ADD POSTS
    if request.method=='POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            form = PostForm()

    else:
        form = PostForm()
    #FORM TO ADD COMMENTS
    if request.POST.get('post_id'):
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        user = request.user
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post,user =user,body=comment)

    posts = Post.objects.all().order_by('created_at').reverse()
    comments = Comment.objects.all()
    my_requests = RequestFriend.objects.filter(send_to = request.user)
    return render(request, 'parts/index.html',context={
        'form': form,
        'posts':posts,
        'comments':comments,
        'my_requests':my_requests,
    } )


def like_post(request):
    postid = request.GET.get('postID')#from user
    post = Post.objects.get(id=postid)#from database
    user = User.objects.get(username=request.user)
    if user not in post.reactions.all():
        post.reactions.add(user)
        post.save()
    else:
        post.reactions.remove(user)
        post.save()
    return JsonResponse({'like':f'{post.number_of_likes}'})


def delete_post(request):
    postid = request.GET.get('postID')#from user
    print(postid,"*"*50)
    post = Post.objects.filter(id=postid)#from database
    if post.exists():
        post.delete()
    return HttpResponse('deleted successfully')
