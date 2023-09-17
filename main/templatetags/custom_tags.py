from django import template
from accounts.models import RequestFriend


register = template.Library()

@register.simple_tag
def display_requests(request):
    my_request = RequestFriend.objects.filter(send_to = request.user)
    request_count = my_request.count()
    return {'requests':my_request,'count':request_count,}

@register.simple_tag
def my_outcoming_request(request):
    my_request = RequestFriend.objects.filter(send_from = request.user)
    request_count = my_request.count()
    return {'requests':my_request,'count':request_count,}