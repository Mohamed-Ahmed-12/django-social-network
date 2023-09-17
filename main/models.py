from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User , on_delete= models.CASCADE)
    description = models.TextField(verbose_name="Post Description" ,max_length=200 , null=False, blank=False)
    photo1 = models.ImageField(verbose_name="Post photo ",upload_to ='postphoto/%y/%m/%d', blank=True ,null=True)
    created_at = models.DateTimeField(auto_now_add=True , editable=False , null=False)
    reactions = models.ManyToManyField(User , related_name="likes")
    active = models.BooleanField(default=True) 
    def __str__(self):
        return f"{self.id , self.user}" 
    class Meta:
        ordering = ('-created_at',)
    
    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()
    @property
    def number_of_likes(self):
        return self.reactions.count()


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(verbose_name="Comment" , max_length=200,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user) + f" Comment on post {self.post.id} of " + str(self.post.user)

class Share(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Who Make Share',related_name='shareowner')
    body = models.TextField(verbose_name="Share Description" , max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user) + f" share post of {self.post.id} " + str(self.post.user)

'''
class Story(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    story = models.FileField(upload_to ='stories/%y/%m/%d', blank=True ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.owner.username
'''