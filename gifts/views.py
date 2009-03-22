from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from wedding.gifts.models import Gift, Category

def index(request):
    categories = Category.objects.all()
    return render_to_response('gifts/index.html', { 'categories': categories })
    
def reserve(request):
    try:
        gift = Gift.objects.get(slug=request.POST['slug'])
        gift.reserved = True
        gift.save()
    except (Gift.DoesNotExist):
        pass
        
    return HttpResponseRedirect('/gifts/#gift-%s' % gift.id)