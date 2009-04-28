from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from wedding.guests.models import Group

def index(request):
    return render_to_response('guests/index.html', { 'error': False })
    
def stage2(request):
    try:
        group = Group.objects.get(email=request.POST['email'])
        guests = group.guest_set.all()
        return render_to_response('guests/stage2.html', { 'group': group, 'guests': guests })
    except (KeyError, Group.DoesNotExist):
        return render_to_response('guests/index.html', { 'error': True })

def save(request):
    try:
        group = Group.objects.get(email=request.POST['email'])
        for guest in group.guest_set.all():            
            guest.attending_ceremony = true_or_false(request.POST, ('%s_ceremony' % guest.id))
            guest.attending_meal = true_or_false(request.POST, ('%s_meal' % guest.id))
            guest.attending_reception = true_or_false(request.POST, ('%s_reception' % guest.id))
            guest.save()
            
        group.rsvp_received = True
        group.save()
        return HttpResponseRedirect(reverse('wedding.guests.views.confirmed'))
    except (Group.DoesNotExist):
        return render_to_response('guests/index.html', { 'error': True })
        
def confirmed(request):
    return render_to_response('guests/confirmed.html')
    
def true_or_false(request, key):
    try:
        if (request[key] == '1'):
            return True
        else:
            return False
    except (KeyError):
        return False
