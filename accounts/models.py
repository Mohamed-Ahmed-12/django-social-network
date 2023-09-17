from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to ='usersphoto/%y/%m/%d') #year month day
    mobile = models.CharField(verbose_name="Phone", max_length=11, null=True)
    bio = models.TextField(null=True , max_length=50)
    gender = models.CharField(choices=[('Male','Male'),('Female','Female')] ,blank=True,null=True,max_length=6)
    country = models.CharField(null=True ,max_length=15)
    created_at = models.DateTimeField(auto_now_add=True , editable=False , null=False )
    friends = models.ManyToManyField(User , related_name="Friends",blank=True)
    slug = models.SlugField(verbose_name="Username Slug",unique=True,blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.user.username

    #this signal create profile when user make sign up     
    def create_profile(sender , **kwargs):
        if kwargs['created']:
            profile = Profile.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile , sender=User)

    #override this method to save slug field from another field in User model and add defult image if not exist
    def save(self ,*args ,**kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile ,self).save(*args,**kwargs)
        
class RequestFriend(models.Model):
    send_from = models.ForeignKey(User , on_delete=models.CASCADE , related_name='sender')
    send_to = models.ForeignKey(User , on_delete=models.CASCADE , related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True , editable=False , null=False )
    class Meta:
        ordering = ["created_at"]
        unique_together = ('send_from', 'send_to',)
    def __str__(self):
        return str(self.send_from) + " send request to " + str(self.send_to)




