from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from wedding.guests.models import Guest

def index(request):
    return render_to_response('guests/index.html')
    
def stage2(request):
    try:
        guest = Guest.objects.get(email=request.POST['email'])
        return render_to_response('guests/stage2.html', { 'guest': guest })
    except (KeyError, Guest.DoesNotExist):
        return render_to_response('guests/index.html', { 'error': True })

def save(request):
    try:
        guest = Guest.objects.get(email=request.POST['email'])
        guest.attending_ceremony = true_or_false(request.POST['ceremony'])
        guest.attending_meal = true_or_false(request.POST['meal'])
        guest.attending_reception = true_or_false(request.POST['reception'])
        guest.save()
        
        return HttpResponseRedirect(reverse('wedding.guests.views.confirmed'))
    except (KeyError, Guest.DoesNotExist):
        return render_to_response('guests/index.html', { 'error': True })
        
def confirmed(request):
    return render_to_response('guests/confirmed.html')
    
def true_or_false(value):
    if (value == '1'):
        return True
    else:
        return False